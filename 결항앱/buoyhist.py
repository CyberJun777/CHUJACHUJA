import subprocess,os,json,datetime,threading,queue,time
import sys
HOURS=sys.argv[1].split(',')
K=os.environ['KMA_API_KEY']; OUT='buoy_hist.jsonl'
done=set()
if os.path.exists(OUT):
    for l in open(OUT): done.add(json.loads(l)['tm'])
q=queue.Queue(); d=datetime.date(2022,12,1)
while d<=datetime.date(2026,5,31):
    for h in HOURS:
        tm=d.strftime('%Y%m%d')+h+'00'
        if tm not in done: q.put(tm)
    d+=datetime.timedelta(1)
lock=threading.Lock(); f=open(OUT,'a'); cnt=[0,0]
def work():
    while True:
        try: tm=q.get_nowait()
        except queue.Empty: return
        rec=None
        for i in range(40):
            r=subprocess.run(['curl','-sS','-m','3','--tls-max','1.2','--ciphers','DEFAULT@SECLEVEL=0','-w','\n%{http_code}',f'https://apihub.kma.go.kr/api/typ01/url/sea_obs.php?tm={tm}&stn=22184&help=0&authKey={K}'],capture_output=True)
            t=r.stdout.decode('euc-kr','ignore'); code=t.rsplit('\n',1)[-1]
            if code=='200':
                rec={'tm':tm,'wh':None}
                for ln in t.splitlines():
                    if ln.startswith('B,'):
                        x=[s.strip() for s in ln.split(',')]
                        rec=dict(tm=tm,obs=x[1],wh=float(x[6]),ws=float(x[8]),gst=float(x[9]))
                break
            if code in('403','401','429'): rec={'tm':tm,'err':code}; break
        with lock:
            if rec and 'err' not in rec: f.write(json.dumps(rec)+'\n'); f.flush(); cnt[0]+=1
            else: cnt[1]+=1
            if (cnt[0]+cnt[1])%50==0: print(time.strftime('%H:%M:%S'),'ok',cnt[0],'fail',cnt[1],'left',q.qsize(),flush=True)
ts=[threading.Thread(target=work) for _ in range(8)]
[t.start() for t in ts]; [t.join() for t in ts]
print('DONE ok',cnt[0],'fail',cnt[1])
