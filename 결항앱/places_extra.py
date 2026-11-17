# 관광지 사진·자료 덧붙임. 원본 화면 스크립트와 요소 id는 그대로 두고, 선택 카드(#pick)와 목록(#plist) 뒤에 덧붙인다.
# 사진: 한국관광공사 국문 관광정보 서비스(TourAPI) 제공, 공공누리 제1유형(출처표시). photos/ 폴더의 실제 현장 사진만 쓴다.
# 사진이나 자료를 더할 때는 PLACES에 항목을 추가하고 python3 mkguide.py, python3 refresh.py 순으로 다시 만든다.
import base64, json, os
KTO='한국관광공사'
PLACES={
 '대왕산 황금길':{'ph':[('hwanggeumgil','제주올레 18-2코스 대왕산 황금길 안내판')],
   't':'하추자 올레(제주올레 18-2코스)는 신양항에서 졸복산, 대왕산 황금길, 묵리슈퍼, 추자교를 지나 추자면사무소까지 이어집니다. 총 9.7km, 3~4시간쯤 걸립니다.','src':'한국관광공사 「제주올레 18-2코스 하추자 올레」'},
 '대왕산':{'t':'하추자 올레(제주올레 18-2코스)가 몽돌해안과 맞닿은 마을길을 지나 졸복산과 대왕산을 오르내립니다. 산꼭대기에서 하추자 앞바다가 내려다보입니다.','src':'한국관광공사 「제주올레 18-2코스 하추자 올레」'},
 '졸복산':{'t':'하추자 올레(제주올레 18-2코스)가 신양항을 떠나 처음 오르는 산으로, 이어서 대왕산 황금길로 넘어갑니다.','src':'한국관광공사 「제주올레 18-2코스 하추자 올레」'},
 '신양항':{'ph':[('sinyanghang','신양항 여객선 대합실')],
   't':'하추자 올레(제주올레 18-2코스)의 시작점입니다. 여기서 졸복산과 대왕산 황금길로 길이 이어집니다.','src':'한국관광공사 「제주올레 18-2코스 하추자 올레」'},
 '모진이몽돌해변':{'ph':[('mojini1','모진이몽돌해변 입구'),('mojini2','파도에 구르는 몽돌'),('mojini3','해변으로 내려가는 길')],
   't':'모래 없이 동글동글한 돌로만 이루어진 해변입니다. 밀려오는 파도에 몽돌이 구르는 소리가 아름다운 곳으로 꼽힙니다. 주소는 추자면 신양4길 18.','src':'한국관광공사 「모진이몽돌해변」(원출처 비짓제주)'},
 '상추자도항':{'ph':[('sangchuja1','상추자도항'),('sangchuja2','상추자도항의 추자도 조형물')],
   't':'오목한 만에 자리한 항구로 제주올레 18-1코스의 시작점입니다. 여객선 터미널이 있어 제주 본섬과 추자도를 잇는 뱃길의 중심이고, 올레길을 따라가면 최영장군 사당과 나바론 절벽을 만납니다.','src':'한국관광공사 「상추자항」'},
 '제주최영장군사당':{'t':'제주특별자치도 기념물로 지정된 사당입니다. 제주올레 18-1코스가 상추자도항에서 이곳으로 이어집니다.','src':'위키백과 「최영장군 사당」, 한국관광공사 「상추자항」'},
}
COURSE={'h':'신양2리를 지나는 하추자 올레','k':'제주올레 18-2코스 · 9.7km · 3~4시간',
 'ph':[('olle182a','하추자 올레 18-2코스의 정자와 바다'),('olle182b','하추자 올레 18-2코스의 정자'),('olle182c','하추자 올레 18-2코스의 바다 전망대')],
 't':'신양항에서 추자면사무소까지 해안길과 산, 마을을 잇는 길입니다. 몽돌해안과 맞닿은 마을길을 지나 졸복산과 대왕산을 오르내리며, 신양항, 졸복산, 대왕산 황금길, 묵리슈퍼, 추자교를 차례로 거칩니다.','src':'한국관광공사 「제주올레 18-2코스 하추자 올레」'}
CSS='''
.px{grid-column:1/-1;margin-top:10px;min-width:0}
.px-row{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding-bottom:4px}
.px-fig{margin:0;flex:0 0 100%;scroll-snap-align:start;min-width:0}
.px-row.many .px-fig{flex-basis:86%}
.px-fig img{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:14px;background:var(--none)}
.px-fig figcaption,.pick .px-src,.px-src{color:var(--muted);font-size:12.5px;line-height:1.5;margin:5px 0 0}
.pick .px-t,.px-t{margin:10px 0 0;font-size:15px;line-height:1.65}
.pick .px-none,.px-none{margin:8px 0 0;color:var(--muted);font-size:13px;line-height:1.5}
.px-course{margin:0 0 16px;padding:14px;border-radius:16px;background:var(--surface);border:1px solid var(--line)}
.px-course h3{margin:0;font-size:17px;line-height:1.4}.px-course .k{color:var(--muted);font-size:13.5px;margin:2px 0 10px}
.plist small .px-b{color:var(--sea);font-weight:700}
'''
JS='''
(function(){
  var X=/*PX*/null,$=function(id){return document.getElementById(id)};
  function figs(a){return '<div class="px-row'+(a.length>1?' many':'')+'">'+a.map(function(p){return '<figure class="px-fig"><img loading="lazy" src="'+p.s+'" alt="'+p.a+'"><figcaption>'+p.a+' · 사진 '+X.c+'</figcaption></figure>'}).join('')+'</div>'}
  function body(e){return (e.ph?figs(e.ph):'')+(e.t?'<p class="px-t">'+e.t+'</p><p class="px-src">자료 출처: '+e.src+'</p>':'')}
  function pick(){var el=$('pick');if(!el||el.querySelector('.px'))return;var b=el.querySelector('b');if(!b||!b.firstChild)return;
    var e=X.p[b.firstChild.nodeValue],d=document.createElement('div');d.className='px';
    d.innerHTML=(e?body(e):'')+(e&&e.ph?'':'<p class="px-none">이곳은 아직 사진이 없습니다. 사용 허가가 확인된 실제 현장 사진만 싣습니다.</p>');el.appendChild(d)}
  function list(){var el=$('plist');if(!el)return;[].forEach.call(el.querySelectorAll('button'),function(b){var n=b.querySelector('span'),s=b.querySelector('small');
    if(!n||!s||s.querySelector('.px-b'))return;var e=X.p[n.textContent];if(e&&e.ph){var m=document.createElement('span');m.className='px-b';m.textContent=' · 사진';s.appendChild(m)}})}
  function course(){var h=$('places');if(!h||document.querySelector('.px-course'))return;var c=X.course,d=document.createElement('div');d.className='px-course';
    d.innerHTML='<h3>'+c.h+'</h3><div class="k">'+c.k+'</div>'+body(c);h.parentNode.insertBefore(d,h.nextSibling)}
  function all(){pick();list();course()}
  if(window.MutationObserver){['pick','plist'].forEach(function(id){var el=$(id);if(el)new MutationObserver(all).observe(el,{childList:true})})}
  all();
})();
'''
def _img(k):
    return 'data:image/jpeg;base64,'+base64.b64encode(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'photos',k+'.jpg'),'rb').read()).decode()
def _e(e):
    o={k:v for k,v in e.items() if k!='ph'}
    if e.get('ph'): o['ph']=[{'s':_img(k),'a':a} for k,a in e['ph']]
    return o
def apply(t):
    X={'c':KTO+'(공공누리 제1유형)','p':{n:_e(e) for n,e in PLACES.items()},'course':_e(COURSE)}
    blk='<style id="px-css">'+CSS+'</style>\n<script id="px-js">'+JS.replace('/*PX*/null',json.dumps(X,ensure_ascii=False,separators=(',',':')))+'</script>\n'
    i=t.rindex('</body>') if '</body>' in t else len(t)
    return t[:i]+blk+t[i:]
