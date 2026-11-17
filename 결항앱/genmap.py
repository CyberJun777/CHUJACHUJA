# osm_chuja.json(오픈스트리트맵, ODbL) → map.json : 추자도 해안선·도로·관광지를 SVG 좌표로 변환
import json,math
j=json.load(open('osm_chuja.json'))['elements']
LAT0,LAT1,LON0,LON1=33.922,33.972,126.276,126.350
W=1000; kx=W/((LON1-LON0)*math.cos(math.radians(33.95))); H=round((LAT1-LAT0)*kx*1.0)
ky=kx
def P(lat,lon): return (round((lon-LON0)*math.cos(math.radians(33.95))*kx,1), round((LAT1-lat)*ky,1))
def inb(g): return any(LAT0-0.01<p['lat']<LAT1+0.01 and LON0-0.01<p['lon']<LON1+0.01 for p in g)
# coastline: stitch ways into rings
segs=[[(p['lat'],p['lon']) for p in e['geometry']] for e in j if e['type']=='way' and e.get('tags',{}).get('natural')=='coastline' and inb(e['geometry'])]
rings=[]
while segs:
    r=segs.pop(0); ch=True
    while r[0]!=r[-1] and ch:
        ch=False
        for i,s in enumerate(segs):
            if s[0]==r[-1]: r+=s[1:]; segs.pop(i); ch=True; break
            if s[-1]==r[-1]: r+=s[::-1][1:]; segs.pop(i); ch=True; break
            if s[-1]==r[0]: r=s[:-1]+r; segs.pop(i); ch=True; break
            if s[0]==r[0]: r=s[::-1][:-1]+r; segs.pop(i); ch=True; break
    rings.append(r)
def d(pts,close=False):
    out=[];last=None
    for lat,lon in pts:
        p=P(lat,lon)
        if last and abs(p[0]-last[0])<0.8 and abs(p[1]-last[1])<0.8: continue
        out.append(('M' if not out else 'L')+f'{p[0]:g} {p[1]:g}'); last=p
    return ''.join(out)+('Z' if close else '')
land=''.join(d(r,r[0]==r[-1]) for r in rings)
print('rings',len(rings),'closed',sum(r[0]==r[-1] for r in rings))
road='';trail='';pier=''
for e in j:
    if e['type']!='way' or not inb(e['geometry']): continue
    t=e.get('tags',{}); g=[(p['lat'],p['lon']) for p in e['geometry']]
    hw=t.get('highway')
    if hw in('secondary','tertiary','residential','living_street','service','track'): 
        if hw=='service' and len(g)<4: continue
        road+=d(g)
    elif hw in('path','footway','steps'): trail+=d(g)
    elif t.get('man_made') in('pier','breakwater'): pier+=d(g)
CAT={'ferry_terminal':'항구','lighthouse':'전망','viewpoint':'전망','peak':'산','beach':'해변','wayside_shrine':'유적','archaeological_site':'유적'}
SKIP={'큰지산','막가채산','작은산','앞산','처녀당','용둥봉','큰산'}
pois=[];seen=set()
for e in j:
    t=e.get('tags',{}); n=t.get('name')
    if not n or n in seen or n in SKIP: continue
    k=t.get('amenity') if t.get('amenity')=='ferry_terminal' else t.get('man_made') if t.get('man_made')=='lighthouse' else t.get('tourism') if t.get('tourism')=='viewpoint' else t.get('natural') if t.get('natural') in('peak','beach') else t.get('historic')
    if k not in CAT: continue
    if e['type']=='node': lat,lon=e['lat'],e['lon']
    else: b=e['bounds']; lat,lon=(b['minlat']+b['maxlat'])/2,(b['minlon']+b['maxlon'])/2
    if not (LAT0<lat<LAT1 and LON0<lon<LON1): continue
    x,y=P(lat,lon); seen.add(n)
    pois.append(dict(n=n,c=CAT[k],x=x,y=y,ele=t.get('ele'),isl='상추자' if lon<126.305 else '하추자'))
vil=[dict(n=e['tags']['name'],x=P(e['lat'],e['lon'])[0],y=P(e['lat'],e['lon'])[1]) for e in j if e['type']=='node' and e.get('tags',{}).get('place')=='village']
# 신양2리: 이장님 답사 인터뷰와 공개 자료에 나온 명소. approx=True 는 좌표가 지도 자료에 없어 설명을 근거로 잡은 추정 위치.
SY={'대왕산':'이장님이 꼽은 신양2리 대표 명소. 올레 18-2코스가 지나갑니다.','졸복산':'올레 18-2코스가 넘는 봉우리. 하추자 앞바다가 내려다보입니다.','석두청산':'정자가 있는 올레 18-2코스 경유지.'}
for p in pois:
    if p['n'] in SY: p['v']='신양2리'; p['d']=SY[p['n']]
for n,c,lat,lon,dsc in [('장작평사','해변',33.9372,126.3262,'추자십경의 하나. 석두리 포구에 펼쳐진 자갈 해변으로 주민들은 진작지라고 부릅니다.'),
                        ('대왕산 황금길','전망',33.9351,126.3206,'올레 18-2코스의 백미로 꼽히는 구간. 중간 스탬프가 있습니다.'),
                        ('용둠벙','유적',33.9362,126.3196,'대왕산의 못. 용이 살다 승천했다는 전설이 있고, 이장님이 숨은 명소로 꼽았습니다.')]:
    x,y=P(lat,lon); pois.append(dict(n=n,c=c,x=x,y=y,ele=None,isl='하추자',v='신양2리',d=dsc,approx=True))
pois.sort(key=lambda p:(p.get('v')!='신양2리',p['isl']!='하추자',p['c'],p['n']))
m=dict(w=W,h=H,land=land,road=road,trail=trail,pier=pier,pois=pois,vil=vil)
json.dump(m,open('map.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
import os;print(W,H,len(land),len(road),len(trail),os.path.getsize('map.json'));[print(p) for p in pois];print(vil)
