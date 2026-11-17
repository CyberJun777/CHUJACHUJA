import os,json,urllib.parse,urllib.request,time,sys
KEY=os.environ['ShipmentKEY']
def call(path,**p):
    q={'pageNo':1,'numOfRows':1000,'dataType':'JSON'}; q.update(p)
    k=KEY if '%' in KEY else urllib.parse.quote(KEY,safe='')
    url=f'https://apis.data.go.kr/B554035/{path}?serviceKey={k}&'+urllib.parse.urlencode(q)
    for i in range(4):
        try:
            with urllib.request.urlopen(url,timeout=40) as r: t=r.read().decode('utf-8','replace')
            try: return json.loads(t)
            except Exception: return {'raw':t[:500]}
        except urllib.error.HTTPError as e:
            return {'http':e.code,'raw':e.read().decode('utf-8','replace')[:500].replace(KEY,'***')}
        except Exception as e:
            err=str(e).replace(KEY,'***'); time.sleep(2)
    return {'err':err}

def day(ymd):
    out=[];pg=1
    while True:
        r=call('oprt-schd-info-v2/get-oprt-schd-info-v2',rlvtYmd=ymd,pageNo=pg)
        resp=r.get('response')
        if not resp: return {'error':r}
        if resp['header']['resultCode']!='200': return {'code':resp['header']['resultCode'],'items':out}
        b=resp['body']; it=b['items']['item']
        if isinstance(it,dict): it=[it]
        out+=it
        if len(out)>=int(b.get('totalCount',0)) or not it: break
        pg+=1
    return {'code':'200','items':out}
