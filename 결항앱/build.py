import csv,collections,json,datetime,urllib.request,sys
sys.path.insert(0,'.')
from api import day
F='../file/oper.utf8.csv'
SHIPS=[('santa','산타모니카','진도-제주','진도 ↔ 상추자 ↔ 제주','쾌속선'),('songlim','송림블루오션','제주-완도','제주 ↔ 추자 ↔ 완도','카페리'),('queen','퀸스타2호','제주-우수영','제주 ↔ 추자 ↔ 우수영','쾌속선')]
rows=list(csv.DictReader(open(F,encoding='utf-8')))
out={'ships':[]}
for key,name,route,label,kind in SHIPS:
    rr=[r for r in rows if r['여객선명']==name and r['면허항로명']==route]
    days=collections.defaultdict(lambda:{'n':0,'c':0,'x':0})
    for r in rr:
        d=days[r['일자']]
        if r['운항여부']=='비운': d['x']+=1
        else:
            d['n']+=1; d['c']+= r['운항여부']=='통제'
    ds=sorted(days)
    mon=[[0,0] for _ in range(12)]     # sailings, controlled
    cond={'y1':[[0,0] for _ in range(4)],'y0':[[0,0] for _ in range(4)]}  # by season: after controlled day / after normal day (day-level)
    dayrate=[[0,0] for _ in range(12)]
    ym=collections.defaultdict(lambda:[0,0])
    S=lambda m:{12:0,1:0,2:0,3:1,4:1,5:1,6:2,7:2,8:2,9:3,10:3,11:3}[m]
    tot=[0,0,0]
    for dstr in ds:
        d=days[dstr]; m=int(dstr[5:7]); tot[2]+=d['x']
        if d['n']==0: continue
        mon[m-1][0]+=d['n']; mon[m-1][1]+=d['c']; tot[0]+=d['n']; tot[1]+=d['c']
        hit=d['c']>0
        dayrate[m-1][0]+=1; dayrate[m-1][1]+=hit
        ym[dstr[:7]][0]+=d['n']; ym[dstr[:7]][1]+=d['c']
        prev=(datetime.date.fromisoformat(dstr)-datetime.timedelta(1)).isoformat()
        p=days.get(prev)
        if p and p['n']>0:
            b=cond['y1' if p['c']>0 else 'y0'][S(m)]; b[0]+=1; b[1]+=hit
    # last 365 days of record daily strip: 0 normal,1 partial,2 all controlled,3 no service
    strip=[]
    end=datetime.date.fromisoformat(ds[-1])
    for i in range(364,-1,-1):
        k=(end-datetime.timedelta(i)).isoformat(); d=days.get(k)
        strip.append(3 if (not d or d['n']==0) else (0 if d['c']==0 else (2 if d['c']==d['n'] else 1)))
    out['ships'].append(dict(key=key,name=name,route=label,kind=kind,first=ds[0],last=ds[-1],sail=tot[0],ctrl=tot[1],off=tot[2],mon=mon,dayrate=dayrate,cond=cond,ym=sorted((k,v[0],v[1]) for k,v in ym.items()),strip=''.join(map(str,strip)),stripEnd=ds[-1]))
    print(name,ds[0],ds[-1],tot,'cond',cond)
# live
def g(u):
    return json.loads(urllib.request.urlopen('http://wind.komsa.or.kr/monitor/'+u,timeout=30).read().decode())
live={'stations':[]}
for sid,nm in [(9654,'제주여객선터미널'),(9652,'제주항 서방파제'),(59126,'완도여객선터미널')]:
    try:
        s=g(f'get_site_info.do?station_id={sid}'); a=g(f'get_apiList.do?station_id={sid}'); w=g(f'get_api.do?station_id={sid}')
        mi=s['maxInfo']
        live['stations'].append(dict(name=nm,time=mi['observation_time'],wind=mi['wind_speed'],dir=float(mi['wind_direction']),gust1=mi['wind_gust_1min_max'],gust10=mi['wind_gust_10min_max'],max=float(mi['max_wind_speed']),oper=a.get('lastScrCn'),sick=a.get('totalIndex'),warn=w.get('status') or json.dumps(w,ensure_ascii=False)[:200],notices=a.get('scroll_list')))
    except Exception as e: print('live fail',nm,e)
print(json.dumps(live,ensure_ascii=False))
today=sys.argv[1]
r=day(today); sch=[]
for x in r.get('items',[]):
    if x['psnshp_nm'] in ('산타모니카','송림블루오션','퀸스타2호','엔젤') and (x['lcns_seawy_nm'] in ('진도-제주','제주-완도','제주-우수영')):
        sch.append(dict(t=str(x['sail_tm']).zfill(4),ship=x['psnshp_nm'],frm=x['oport_nm'],to=x['dest_nm'],rt=x['nvg_seawy_nm'],se=x['nvg_se_nm'],st=x['nvg_stts_nm'],why=x['cntrl_rsn_nm'] or x['cnls_etc_rsn'] or x['nnavi_rsn_nm']))
sch.sort(key=lambda s:s['t']); live['schedule']=sch; live['date']=today; live['code']=r.get('code')
live['fetched']=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M')
out['live']=live
json.dump(out,open('data.json','w'),ensure_ascii=False,separators=(',',':'))
print(json.dumps(sch,ensure_ascii=False)); import os; print(os.path.getsize('data.json'))
