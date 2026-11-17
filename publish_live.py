# 결항앱/data.json 의 live(오늘 운항·부이·예보)만 꺼내 data/live.json 으로 쓴다. 앱이 이 파일을 받아 간다.
# 사용: python3 publish_live.py [data.json 경로]   (기본: 결항앱/data.json)
import json,sys,os,re
HERE=os.path.dirname(os.path.abspath(__file__))
src=sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,'결항앱','data.json')
L=json.load(open(src,encoding='utf-8'))['live']
assert re.fullmatch(r'\d{4}-\d\d-\d\d \d\d:\d\d',L['fetched']) and re.fullmatch(r'\d{8}',L['date'])
assert L['stations'] and isinstance(L['schedule'],list)
out=os.path.join(HERE,'data','live.json'); os.makedirs(os.path.dirname(out),exist_ok=True)
old=json.load(open(out,encoding='utf-8')) if os.path.exists(out) else None
if old and old['fetched']>=L['fetched']: print('이미 최신:',old['fetched']); sys.exit(0)
json.dump(L,open(out,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('data/live.json 갱신:',L['fetched'],'부이' if L.get('buoy') else '부이 없음','예보',len(L.get('fc',[])))
