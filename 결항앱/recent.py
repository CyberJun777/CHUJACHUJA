import json,os,subprocess,sys
from api import day
from backtest import prob,d
K=os.environ.get('KMA_API_KEY','')
def buoy(tm):
    for i in range(60):
        p=subprocess.run(['curl','-sS','-m','4','--tls-max','1.2','--ciphers','DEFAULT@SECLEVEL=0','-w','\n%{http_code}',f'https://apihub.kma.go.kr/api/typ01/url/sea_obs.php?tm={tm}&stn=22184&help=0&authKey={K}'],capture_output=True)
        t=p.stdout.decode('euc-kr','ignore')
        if t.rsplit('\n',1)[-1]=='200':
            for ln in t.splitlines():
                if ln.startswith('B,'):
                    f=[x.strip() for x in ln.split(',')]
                    return f[1],float(f[6]),float(f[8])
            return None
    return None
S={s['name']:s for s in d['ships']}
out=[]
for ymd in sys.argv[1:]:
    b=buoy(ymd+'1000') if ymd!=sys.argv[-1] or True else None
    r=day(ymd); rows=[x for x in r.get('items',[]) if x['psnshp_nm'] in ('산타모니카','송림블루오션') and x['lcns_seawy_nm'] in ('진도-제주','제주-완도')]
    print(ymd,'부이10시',b,'API',r.get('code'))
    for nm in ('산타모니카','송림블루오션'):
        xs=sorted(rows,key=lambda x:str(x['sail_tm']).zfill(4))
        xs=[x for x in xs if x['psnshp_nm']==nm]
        st=[(str(x['sail_tm']).zfill(4),x['nvg_se_nm'],x['nvg_stts_nm'],x['cntrl_rsn_nm'] or x['nnavi_rsn_nm'] or x['cnls_etc_rsn']) for x in xs]
        p=round(prob(S[nm]['pts'],b[1],b[2])*100) if b and b[1]>-90 else None
        print('  ',nm,'앱 확률',p,'%',st)
        out.append(dict(ymd=ymd,ship=nm,buoy=b,p=p,sail=st))
json.dump(out,open('recent_check.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
