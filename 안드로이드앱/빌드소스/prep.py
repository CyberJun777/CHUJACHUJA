import re,subprocess,os,sys,hashlib
# 화면 원본: 저장소의 결항앱/chuja-guide.html (refresh.py가 만든 것)
HERE=os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
src=open(os.path.join(HERE,'..','..','결항앱','chuja-guide.html'),encoding='utf-8').read()
os.makedirs('app/assets/fonts',exist_ok=True)
chars=set(map(ord,src))
UA='Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Mobile Safari/537.36'
links=re.findall(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/css2[^"]+)">',src)
allcss=[];n=0;tot=0
def inrange(rng):
    for part in rng.split(','):
        part=part.strip()[2:]
        if '-' in part: a,b=part.split('-'); a,b=int(a,16),int(b,16)
        elif '?' in part: a=int(part.replace('?','0'),16); b=int(part.replace('?','F'),16)
        else: a=b=int(part,16)
        if any(a<=c<=b for c in chars): return True
    return False
for l in links:
    css=subprocess.run(['curl','-fsS','-m','60','-A',UA,l],capture_output=True,text=True,check=True).stdout
    for blk in re.findall(r'@font-face\s*\{[^}]+\}',css):
        m=re.search(r'unicode-range:\s*([^;]+);',blk)
        if m and not inrange(m.group(1)): continue
        u=re.search(r'url\((https://[^)]+)\)',blk).group(1)
        fn=hashlib.md5(u.encode()).hexdigest()[:12]+'.woff2'
        p='app/assets/fonts/'+fn
        if not os.path.exists(p): subprocess.run(['curl','-fsS','-m','60','-o',p,u],check=True)
        tot+=os.path.getsize(p);n+=1
        allcss.append(blk.replace(u,'fonts/'+fn))
print(n,'font files',tot//1024,'KB')
body=src
for l in links: body=body.replace('<link rel="stylesheet" href="%s">'%l,'')
body=body.replace('<link rel="preconnect" href="https://fonts.googleapis.com">','')
assert 'googleapis' not in body
# 매일 갱신: (1) 기기에 저장해 둔 최신 자료가 내장 자료보다 새것이면 그것으로 시작, (2) 끝에 live-update.js를 붙여 깃허브에서 새 자료를 받는다.
ANCHOR="\n  var $=function(id){return document.getElementById(id)};"
i=body.index('var D={'); j=body.index(ANCHOR,i)
assert body.count('var D={')==1 and j-i>1000
HOOK="\n  try{var __L=JSON.parse(localStorage.getItem('sinyang.live'));if(__L&&__L.fetched>D.live.fetched&&__L.stations&&__L.stations.length&&__L.schedule)D.live=__L}catch(e){}"
body=body[:j]+HOOK+body[j:]
CSS='<style>.live-stale{margin:12px 16px 0;padding:10px 12px;border-radius:12px;background:var(--warn-soft);color:var(--ink);font-size:13px;line-height:1.5}#view-ferry .live-stale{margin:0}</style>'
body+='\n'+CSS+'\n<script>\n'+open('live-update.js',encoding='utf-8').read()+'</script>'
head='<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<style>\n'+'\n'.join(allcss)+'\n</style>\n</head>\n<body>\n'
open('app/assets/index.html','w',encoding='utf-8').write(head+body+'\n</body>\n</html>\n')

# 같은 화면을 파일 하나짜리 HTML로도 만든다(아이폰·PC 브라우저용). 글꼴은 내장하지 않고 인터넷에서 받는다.
solo=src[:src.index(ANCHOR,src.index('var D={'))]+HOOK+src[src.index(ANCHOR,src.index('var D={')):]
solo='<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<title>신양愛소리</title>\n</head>\n<body>\n'+solo+'\n'+CSS+'\n<script>\n'+open('live-update.js',encoding='utf-8').read()+'</script>\n</body>\n</html>\n'
open(os.path.join(HERE,'..','..','신양애소리.html'),'w',encoding='utf-8').write(solo)
open(os.path.join(HERE,'..','..','index.html'),'w',encoding='utf-8').write(solo)   # 웹 주소로 열 때 쓰는 같은 파일
print('신양애소리.html',len(solo)//1024,'KB')
