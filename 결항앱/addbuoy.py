import json,sys
d=json.load(open('data.json',encoding='utf-8'))
t=open(sys.argv[1],encoding='euc-kr',errors='ignore').read()
for ln in t.splitlines():
    if ln.startswith('#') or not ln.strip(): continue
    f=[x.strip() for x in ln.split(',')]
    if f[2]=='22184':
        d['live']['buoy']=dict(time=f[1][:4]+'-'+f[1][4:6]+'-'+f[1][6:8]+'T'+f[1][8:10]+':'+f[1][10:12],wh=float(f[6]),wd=float(f[7]),ws=float(f[8]),gst=float(f[9]),tw=float(f[10]))
print(d['live'].get('buoy'))
json.dump(d,open('data.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
