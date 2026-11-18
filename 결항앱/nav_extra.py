# 지도 화면에 "내 위치"(휴대폰 위치 권한)와 관광지별 "길찾기"(카카오맵 웹 링크, 키 필요 없음)를 덧붙인다.
# 내 위치를 켠 채 관광지를 고르면 오픈스트리트맵 길 자료로 걷는 동선을 지도에 그린다(인터넷·키 필요 없음).
# 원본 스크립트·id는 건드리지 않고 #map-full, #pick 을 MutationObserver로 지켜보며 덧붙인다(places_extra와 같은 방식).
import json,math
LAT0,LAT1,LON0,LON1=33.922,33.972,126.276,126.350   # genmap.py와 같은 범위
C=math.cos(math.radians(33.95)); KX=1000/((LON1-LON0)*C)
def ll(x,y): return round(LAT1-y/KX,6), round(LON0+x/(C*KX),6)

CSS='''
.nv-bar{display:flex;align-items:center;gap:10px;margin:10px 0 0;flex-wrap:wrap}
.nv-me{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:7px 14px;font:inherit;font-size:13.5px;font-weight:600;cursor:pointer}
.nv-me[aria-pressed="true"]{background:var(--sea);border-color:var(--sea);color:#fff}
.nv-me svg{width:16px;height:16px;fill:currentColor}
.nv-msg{font-size:12.5px;color:var(--muted);flex:1 1 180px}
.nv-go{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px;grid-column:1/-1}
.nv-go a{display:inline-flex;align-items:center;gap:6px;background:var(--sea);color:#fff;text-decoration:none;border-radius:999px;padding:8px 16px;font-size:14px;font-weight:700}
.nv-go a.alt{background:transparent;color:var(--sea);border:1px solid var(--sea)}
.nv-go small{flex-basis:100%;font-size:12px;color:var(--muted)}
.nv-dot,.nv-route{pointer-events:none}
.nv-ask{flex-basis:100%;background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:12px 14px;font-size:13.5px;line-height:1.55}
.nv-ask p{margin:0 0 10px}
.nv-ask div{display:flex;gap:8px}
.nv-ask button{font:inherit;font-size:13.5px;font-weight:700;border-radius:999px;padding:7px 16px;cursor:pointer;border:1px solid var(--sea)}
.nv-ask .ok{background:var(--sea);color:#fff}.nv-ask .no{background:transparent;color:var(--sea)}
'''

JS='''(function(){
  var G=/*NVG*/null,MU=%(MU)s,RT=null,P=/*NV*/null,$=function(id){return document.getElementById(id)},me=null,watch=null,on=false;
  var K=%(KX)s,C=%(C)s,LAT0=%(LAT0)s,LAT1=%(LAT1)s,LON0=%(LON0)s,LON1=%(LON1)s;
  function xy(lat,lon){return[(lon-LON0)*C*K,(LAT1-lat)*K]}
  function km(a,b,c,d){var R=6371,r=Math.PI/180,x=(d-b)*r*Math.cos((a+c)/2*r),y=(c-a)*r;return R*Math.sqrt(x*x+y*y)}
  function inside(){return me&&me.lat>LAT0-0.005&&me.lat<LAT1+0.005&&me.lon>LON0-0.005&&me.lon<LON1+0.005}
  function msg(t){var m=document.querySelector('.nv-msg');if(m)m.textContent=t}
  function cur(){var b=$('pick')&&$('pick').querySelector('b');return b&&b.firstChild?P[b.firstChild.textContent.trim()]:null}
  function info(){
    if(!on)return;if(!me){msg('위치를 찾는 중입니다…');return}
    var p=cur(),d=p?km(me.lat,me.lon,p[0],p[1]):null;
    function f(m){return m<1000?Math.round(m/10)*10+' m':(m/1000).toFixed(1)+' km'}
    if(inside())msg('파란 점이 지금 계신 곳입니다'+(d!=null?(RT!=null?'. 파란 선이 '+p[2]+'까지 가는 길입니다(약 '+f(RT)+', 걸어서 '+Math.max(1,Math.round(RT/1000*15))+'분쯤, 오르막은 더 걸려요)':'. '+p[2]+'까지 직선으로 약 '+f(d*1000)):'')+'.');
    else msg('지금 추자도 밖에 계셔서 지도에는 표시하지 않습니다'+(d!=null?' ('+p[2]+'까지 약 '+Math.round(d)+' km)':'')+'.');
  }
  function dot(){
    var s=$('map-full')&&$('map-full').querySelector('svg');if(!s)return;
    var o=s.querySelector('.nv-dot');if(o)o.remove();
    route(s);
    if(!on||!inside())return;
    var q=xy(me.lat,me.lon),r=Math.max(4,Math.min(40,(me.acc||30)*K/111320/C)),ns='http://www.w3.org/2000/svg',g=document.createElementNS(ns,'g');
    g.setAttribute('class','nv-dot');
    g.innerHTML='<circle cx="'+q[0]+'" cy="'+q[1]+'" r="'+r+'" fill="#3A6BF0" opacity=".15"/><circle cx="'+q[0]+'" cy="'+q[1]+'" r="7" fill="#3A6BF0" stroke="#fff" stroke-width="3"/>';
    s.appendChild(g);
  }
  // 동선: 길 자료(G.p 좌표×10, G.e 연결)에서 가장 가까운 길 지점끼리 최단 경로를 찾는다.
  var AD=null,NX=null,NY=null;
  function prep(){if(AD)return;var n=G.p.length/2,i;NX=new Float64Array(n);NY=new Float64Array(n);AD=[];
    for(i=0;i<n;i++){NX[i]=G.p[2*i]/10;NY[i]=G.p[2*i+1]/10;AD.push([])}
    for(i=0;i<G.e.length;i+=2){var a=G.e[i],b=G.e[i+1],w=Math.hypot(NX[a]-NX[b],NY[a]-NY[b]);AD[a].push(b,w);AD[b].push(a,w)}}
  function near(x,y){var b=-1,bd=1e18;for(var i=0;i<NX.length;i++){var d=(NX[i]-x)*(NX[i]-x)+(NY[i]-y)*(NY[i]-y);if(d<bd){bd=d;b=i}}return b}
  function path(s,t){var n=NX.length,D=new Float64Array(n).fill(Infinity),F=new Int32Array(n).fill(-1),H=[[0,s]];D[s]=0;
    function up(i){while(i>0){var j=(i-1)>>1;if(H[j][0]<=H[i][0])break;var q=H[i];H[i]=H[j];H[j]=q;i=j}}
    function dn(i){for(;;){var l=2*i+1,r=l+1,m=i;if(l<H.length&&H[l][0]<H[m][0])m=l;if(r<H.length&&H[r][0]<H[m][0])m=r;if(m===i)break;var q=H[i];H[i]=H[m];H[m]=q;i=m}}
    while(H.length){var top=H[0],last=H.pop();if(H.length){H[0]=last;dn(0)}var d=top[0],u=top[1];if(d>D[u])continue;if(u===t)break;
      var a=AD[u];for(var k=0;k<a.length;k+=2){var v=a[k],nd=d+a[k+1];if(nd<D[v]){D[v]=nd;F[v]=u;H.push([nd,v]);up(H.length-1)}}}
    if(!isFinite(D[t]))return null;var out=[];for(var v=t;v!==-1;v=F[v])out.push(v);return out.reverse()}
  function route(s){
    var o=s.querySelector('.nv-route');if(o)o.remove();RT=null;
    var p=cur();if(!G||!on||!me||!inside()||!p)return;prep();
    var a=xy(me.lat,me.lon),b=xy(p[0],p[1]),i=near(a[0],a[1]),j=near(b[0],b[1]),r=path(i,j);if(!r)return;
    var pts=[a].concat(r.map(function(k){return[NX[k],NY[k]]})).concat([b]),L=0;
    for(var k=1;k<pts.length;k++)L+=Math.hypot(pts[k][0]-pts[k-1][0],pts[k][1]-pts[k-1][1]);
    RT=L*MU;
    var ns='http://www.w3.org/2000/svg',g=document.createElementNS(ns,'g'),d=pts.map(function(q,k){return(k?'L':'M')+q[0].toFixed(1)+' '+q[1].toFixed(1)}).join('');
    g.setAttribute('class','nv-route');
    g.innerHTML='<path d="'+d+'" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/><path d="'+d+'" fill="none" stroke="#3A6BF0" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 9" /><path d="'+d+'" fill="none" stroke="#3A6BF0" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>';
    var dt=s.querySelector('.nv-dot');s.insertBefore(g,dt||null);
  }
  function stop(){on=false;if(watch!=null&&navigator.geolocation)navigator.geolocation.clearWatch(watch);watch=null;var b=document.querySelector('.nv-me');if(b)b.setAttribute('aria-pressed','false');msg('');dot()}
  function start(){
    var b=document.querySelector('.nv-me');
    if(!navigator.geolocation){msg('이 기기에서는 위치를 확인할 수 없습니다.');return}
    on=true;b.setAttribute('aria-pressed','true');info();
    watch=navigator.geolocation.watchPosition(function(p){me={lat:p.coords.latitude,lon:p.coords.longitude,acc:p.coords.accuracy};dot();info()},
      function(e){var t=e.code===1?'위치 권한이 꺼져 있습니다. 휴대폰 설정에서 이 앱의 위치 권한을 허용해 주세요.':'위치를 찾지 못했습니다. 잠시 뒤 다시 눌러 주세요.';stop();msg(t)},
      {enableHighAccuracy:true,maximumAge:15000,timeout:20000});
  }
  var agreed=false;
  function ask(){
    if(document.querySelector('.nv-ask'))return;var d=document.querySelector('.nv-bar'),a=document.createElement('div');a.className='nv-ask';a.setAttribute('role','dialog');a.setAttribute('aria-label','위치 정보 이용 동의');
    a.innerHTML='<p><b>위치 정보를 쓸까요?</b><br>지도에 지금 계신 곳을 표시하고 관광지까지 거리를 재는 데만 씁니다. 위치는 휴대폰 밖으로 보내거나 저장하지 않으며, 버튼을 다시 누르면 멈춥니다.</p><div><button type="button" class="ok">동의하고 내 위치 보기</button><button type="button" class="no">취소</button></div>';
    d.appendChild(a);a.querySelector('.ok').focus();
    a.querySelector('.ok').onclick=function(){agreed=true;a.remove();start()};
    a.querySelector('.no').onclick=function(){a.remove();msg('')};
  }
  function bar(){
    var z=$('zoom');if(!z||document.querySelector('.nv-bar'))return;
    var d=document.createElement('div');d.className='nv-bar';
    d.innerHTML='<button type="button" class="nv-me" aria-pressed="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm9 3h-2.07A7 7 0 0 0 13 5.07V3h-2v2.07A7 7 0 0 0 5.07 11H3v2h2.07A7 7 0 0 0 11 18.93V21h2v-2.07A7 7 0 0 0 18.93 13H21v-2zm-9 6a5 5 0 1 1 0-10 5 5 0 0 1 0 10z"/></svg>내 위치</button><span class="nv-msg" role="status"></span>';
    z.parentNode.insertBefore(d,z.nextSibling);
    d.firstChild.onclick=function(){if(on){stop();return}if(agreed){start();return}ask()};
  }
  function go(){
    var el=$('pick');if(!el||el.querySelector('.nv-go'))return;var p=cur();if(!p)return;
    var n=encodeURIComponent(p[2]),w=document.createElement('div');w.className='nv-go';
    w.innerHTML='<a href="https://map.kakao.com/link/to/'+n+','+p[0]+','+p[1]+'" target="_blank" rel="noopener">카카오맵 길찾기</a>'+
      '<a class="alt" href="https://map.kakao.com/link/map/'+n+','+p[0]+','+p[1]+'" target="_blank" rel="noopener">위치만 보기</a>'+
      '<small>카카오맵이 열리면 지금 위치에서 '+p[2]+'까지 가는 길을 안내합니다.'+(p[3]?' 이곳은 위치가 추정이라 근처까지 안내됩니다.':'')+'</small>';
    var px=el.querySelector('.px');el.insertBefore(w,px||null);
    info();
  }
  function all(){bar();go();dot();info()}
  if(window.MutationObserver){['pick','map-full'].forEach(function(id){var e=$(id);if(e)new MutationObserver(all).observe(e,{childList:true})})}
  all();
})();'''

def graph():
    import os,collections
    els=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'osm_chuja.json'),encoding='utf-8'))['elements']
    H={'secondary','tertiary','residential','living_street','service','track','path','footway','steps','unclassified','pedestrian'}
    xyz={};adj=collections.defaultdict(set)
    for w in els:
        if w['type']!='way' or w.get('tags',{}).get('highway') not in H: continue
        for nid,g in zip(w['nodes'],w['geometry']):
            xyz[nid]=(g['lon']-LON0)*C*KX,(LAT1-g['lat'])*KX
        for a,b in zip(w['nodes'],w['nodes'][1:]): adj[a].add(b);adj[b].add(a)
    best=set();seen=set()   # 서로 이어진 가장 큰 길 묶음만 쓴다(끊긴 작은 조각으로 이어 붙이지 않게)
    for s0 in adj:
        if s0 in seen: continue
        comp={s0};st=[s0];seen.add(s0)
        while st:
            u=st.pop()
            for v in adj[u]:
                if v not in seen: seen.add(v);comp.add(v);st.append(v)
        if len(comp)>len(best): best=comp
    ids=sorted(best);ix={n:i for i,n in enumerate(ids)};p=[];e=[]
    for n in ids: p+= [round(xyz[n][0]*10),round(xyz[n][1]*10)]
    for a in ids:
        for b in adj[a]:
            if a<b: e+=[ix[a],ix[b]]
    return dict(p=p,e=e)

def apply(t):
    m=json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'map.json'),encoding='utf-8'))
    P={p['n']:list(ll(p['x'],p['y']))+[p['n'],bool(p.get('approx'))] for p in m['pois']}
    js=JS%dict(KX=KX,C=C,LAT0=LAT0,LAT1=LAT1,LON0=LON0,LON1=LON1,MU=round(111320/KX,4))
    js=js.replace('/*NVG*/null',json.dumps(graph(),separators=(',',':')))
    blk='<style id="nv-css">'+CSS+'</style>\n<script id="nv-js">'+js.replace('/*NV*/null',json.dumps(P,ensure_ascii=False,separators=(',',':')))+'</script>\n'
    i=t.rindex('</body>') if '</body>' in t else len(t)
    return t[:i]+blk+t[i:]
