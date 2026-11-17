# 오늘 실황만 다시 받아 data.json 의 live 를 갱신하고 chuja-ferry.html 을 다시 만든다. (과거 통계·pts 는 그대로)
# 사용: cd /mnt/project-files/결항앱/ && python3 refresh.py   → 그 뒤 chuja-ferry.html 을 같은 Artifact 주소로 게시
import json,os,sys,subprocess,datetime,urllib.request
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from api import day
KST=datetime.timezone(datetime.timedelta(hours=9)); now=datetime.datetime.now(KST)
d=json.load(open('data.json',encoding='utf-8')); old=d['live']; live={'stations':[]}
def g(u): return json.loads(urllib.request.urlopen('http://wind.komsa.or.kr/monitor/'+u,timeout=30).read().decode())
for sid,nm in [(9654,'제주여객선터미널'),(9652,'제주항 서방파제'),(59126,'완도여객선터미널')]:
    try:
        s=g(f'get_site_info.do?station_id={sid}');a=g(f'get_apiList.do?station_id={sid}');w=g(f'get_api.do?station_id={sid}');mi=s['maxInfo']
        live['stations'].append(dict(name=nm,time=mi['observation_time'],wind=mi['wind_speed'],dir=float(mi['wind_direction']),gust1=mi['wind_gust_1min_max'],gust10=mi['wind_gust_10min_max'],max=float(mi['max_wind_speed']),oper=a.get('lastScrCn'),sick=a.get('totalIndex'),warn=w.get('status') or json.dumps(w,ensure_ascii=False)[:200],notices=a.get('scroll_list')))
    except Exception as e: print('KOMSA fail',nm,e)
if not live['stations']: live['stations']=old['stations']; print('KOMSA 전부 실패: 이전 값 유지')
today=now.strftime('%Y%m%d'); r=day(today); sch=[]
for x in r.get('items',[]):
    if x['psnshp_nm'] in ('산타모니카','송림블루오션','퀸스타2호','엔젤') and x['lcns_seawy_nm'] in ('진도-제주','제주-완도','제주-우수영'):
        sch.append(dict(t=str(x['sail_tm']).zfill(4),ship=x['psnshp_nm'],frm=x['oport_nm'],to=x['dest_nm'],rt=x['nvg_seawy_nm'],se=x['nvg_se_nm'],st=x['nvg_stts_nm'],why=x['cntrl_rsn_nm'] or x['cnls_etc_rsn'] or x['nnavi_rsn_nm']))
sch.sort(key=lambda s:s['t']); print('schedule',r.get('code') or r.get('error'),len(sch))
live['schedule']=sch; live['date']=today; live['fetched']=now.strftime('%Y-%m-%d %H:%M')
K=os.environ.get('KMA_API_KEY',''); buoy=None
for hh in (now,now-datetime.timedelta(hours=1)):
    tm=hh.strftime('%Y%m%d%H00')
    for i in range(40):
        p=subprocess.run(['curl','-sS','-m','4','--tls-max','1.2','--ciphers','DEFAULT@SECLEVEL=0','-w','\n%{http_code}',f'https://apihub.kma.go.kr/api/typ01/url/sea_obs.php?tm={tm}&stn=22184&help=0&authKey={K}'],capture_output=True)
        t=p.stdout.decode('euc-kr','ignore')
        if t.rsplit('\n',1)[-1]=='200':
            for ln in t.splitlines():
                if ln.startswith('B,'):
                    f=[x.strip() for x in ln.split(',')]
                    if float(f[6])>-90: buoy=dict(time=f[1][:4]+'-'+f[1][4:6]+'-'+f[1][6:8]+'T'+f[1][8:10]+':'+f[1][10:12],wh=float(f[6]),wd=float(f[7]),ws=float(f[8]),gst=float(f[9]),tw=float(f[10]))
            break
    if buoy: break
print('buoy',buoy)
if buoy: live['buoy']=buoy   # 못 받으면 부이 칸을 숨긴다(오래된 값을 현재값처럼 보이지 않게)
# 해상예보(제주도북부앞바다 12B10302, 추자도 포함 구역): 최신 발표분
fc=[]
t1=(now-datetime.timedelta(hours=20)).strftime('%Y%m%d%H'); t2=now.strftime('%Y%m%d%H')
for i in range(40):
    p=subprocess.run(['curl','-sS','-m','6','--tls-max','1.2','--ciphers','DEFAULT@SECLEVEL=0','-w','\n%{http_code}',f'https://apihub.kma.go.kr/api/typ01/url/fct_afs_do.php?reg=12B10302&tmfc1={t1}&tmfc2={t2}&disp=0&help=0&authKey={K}'],capture_output=True)
    t=p.stdout.decode('euc-kr','ignore')
    if t.rsplit('\n',1)[-1]=='200':
        rows=[]
        for ln in t.splitlines():
            if not ln.startswith('12B10302'): continue
            left,_,wf=ln.partition('"'); x=left.split()
            try: rows.append(dict(fc=x[1],ef=x[2],w1=x[-9],w2=x[-7],s1=float(x[-6]),s2=float(x[-5]),wh1=float(x[-4]),wh2=float(x[-3]),wf=wf.strip('" ')))
            except Exception as e: print('fc parse',e)
        if rows:
            last=max(r['fc'] for r in rows); fc=[r for r in rows if r['fc']==last]
        break
print('forecast',len(fc),fc[0]['fc'] if fc else None)
if fc: live['fc']=fc
d['live']=live
json.dump(d,open('data.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
import skin
h=skin.apply(open('tpl.html',encoding='utf-8').read()).replace('/*DATA*/null',json.dumps(d,ensure_ascii=False,separators=(',',':')))
open('chuja-ferry.html','w',encoding='utf-8').write(h); print('wrote chuja-ferry.html',len(h))
g=open('guide.tpl.html',encoding='utf-8').read().replace('/*DATA*/null',json.dumps(d,ensure_ascii=False,separators=(',',':')))
open('chuja-guide.html','w',encoding='utf-8').write(g); print('wrote chuja-guide.html',len(g))
