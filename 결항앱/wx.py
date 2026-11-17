import json,csv,collections
b={}
for l in open('buoy_hist.jsonl'):
    x=json.loads(l)
    if x.get('wh') is not None and x['wh']>-90 and x['ws']>-90 and x['tm'][8:10]=='10': b[x['tm'][:8]]=(x['wh'],x['ws'])
d=json.load(open('data.json',encoding='utf-8'))
rows=list(csv.DictReader(open('../file/oper.utf8.csv',encoding='utf-8')))
M={'santa':('산타모니카','진도-제주'),'songlim':('송림블루오션','제주-완도'),'queen':('퀸스타2호','제주-우수영')}
for s in d['ships']:
    nm,rt=M[s['key']]; days=collections.defaultdict(lambda:[0,0])
    for r in rows:
        if r['여객선명']==nm and r['면허항로명']==rt and r['운항여부']!='비운':
            k=r['일자'].replace('-',''); days[k][0]+=1; days[k][1]+= r['운항여부']=='통제'
    pts=[[b[k][0],b[k][1],1 if v[1]>0 else 0] for k,v in sorted(days.items()) if k in b]
    s['pts']=pts
    print(nm,len(days),len(pts))
    for lo,hi in [(0,.5),(.5,1),(1,1.5),(1.5,2),(2,2.5),(2.5,3),(3,9)]:
        q=[p for p in pts if lo<=p[0]<hi]; print('  wave',lo,hi,len(q),round(100*sum(p[2] for p in q)/len(q)) if q else None)
    for lo,hi in [(0,4),(4,8),(8,10),(10,12),(12,14),(14,40)]:
        q=[p for p in pts if lo<=p[1]<hi]; print('  wind',lo,hi,len(q),round(100*sum(p[2] for p in q)/len(q)) if q else None)
json.dump(d,open('data.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
