# 관광지 사진·자료 덧붙임. 원본 화면 스크립트와 요소 id는 그대로 두고, 선택 카드(#pick)와 목록(#plist) 뒤에 덧붙인다.
# 자료: 한국민족문화대백과사전(공공누리), 한국관광공사, 이장님 인터뷰, 오픈스트리트맵. 출처를 장소마다 표기한다.
# 사진: 한국관광공사 국문 관광정보 서비스(TourAPI) 제공, 공공누리 제1유형(출처표시). photos/ 폴더의 실제 현장 사진만 쓴다.
# 사진이나 자료를 더할 때는 PLACES에 항목을 추가하고 python3 mkguide.py, python3 refresh.py 순으로 다시 만든다.
import base64, json, os
KTO='한국관광공사'
EK='한국민족문화대백과사전'
S_HA='「하추자도」 - '+EK; S_SANG='「상추자도」 - '+EK; S_GUN='「추자군도」 - '+EK
S_182='한국관광공사 「제주올레 18-2코스 하추자 올레」'; S_181='한국관광공사 「제주올레 18-1코스 상추자 올레」'
S_INT='신양2리 이장님 인터뷰(답사 질의응답, 2026)'; S_OSM='오픈스트리트맵(© OpenStreetMap contributors)'
# 장소 이름은 map.json의 pois 이름과 같아야 한다. info: (항목, 내용), t: 문단, src: 출처. 사실은 출처에 있는 것만 쓴다.
PLACES={
 '대왕산':{'info':[('위치','하추자도 신양2리'),('높이','해발 124.9 m'),('코스','제주올레 18-2코스(하추자 올레)')],
   't':['신양2리를 대표하는 산입니다. 하추자 올레가 몽돌해안과 맞닿은 마을길을 지나 졸복산과 대왕산을 차례로 오르내리고, 산꼭대기에서는 하추자 앞바다가 한눈에 내려다보입니다.',
        '이장님은 신양2리를 찾는 사람들이 주로 올레 18-2코스와 대왕산을 보러 온다고 했고, 마을에서 가장 아끼는 곳으로도 대왕산을 꼽았습니다.',
        '산속과 바닷가에 버려지는 쓰레기가 마을의 큰 걱정입니다. 가져온 쓰레기는 꼭 되가져가 주세요.'],
   'src':[S_HA,S_182,S_INT]},
 '석두청산':{'info':[('위치','하추자도 신양2리'),('높이','해발 94.2 m'),('코스','제주올레 18-2코스(하추자 올레)')],
   't':['하추자 올레 18-2코스가 지나는 신양2리의 봉우리로, 쉬어 갈 수 있는 정자가 있습니다.'],
   'src':[S_OSM]},
 '졸복산':{'info':[('위치','하추자도 신양2리'),('높이','해발 97 m'),('코스','제주올레 18-2코스(하추자 올레)')],
   't':['신양항을 떠난 하추자 올레 18-2코스가 넘는 봉우리입니다. 졸복산을 지나면 대왕산과 대왕산 황금길로 길이 이어집니다.'],
   'src':[S_182,S_OSM]},
 '용둠벙':{'info':[('위치','하추자도 신양2리 대왕산 자락 (지도 위치는 추정)'),('성격','이장님이 꼽은 마을의 숨은 명소')],
   't':['이장님이 관광객은 잘 모르고 주민들만 아는 숨은 명소로 꼽은 곳입니다. 용이 살다가 승천했다는 이야기가 전해지며, 이장님은 "용이 승천하려고 나온 바위" 쪽을 마을에서 아끼는 곳으로 들었습니다.',
        '정확한 위치는 아직 확인하지 못해 지도에는 점선 테두리로 추정 위치를 표시했습니다.'],
   'src':[S_INT]},
 '대왕산 황금길':{'ph':[('hwanggeumgil','제주올레 18-2코스 대왕산 황금길 안내판')],
   'info':[('위치','하추자도 신양2리 대왕산 (지도 위치는 추정)'),('코스','제주올레 18-2코스, 중간 스탬프 지점'),('코스 전체','9.7 km, 3~4시간')],
   't':['하추자 올레 18-2코스에서 손꼽히는 구간입니다. 코스는 신양항에서 시작해 졸복산, 대왕산 황금길, 묵리슈퍼, 추자교를 지나 추자면사무소에서 끝납니다.',
        '안내판에는 신양2리 주민들의 도움으로 18-2코스가 완성됐다는 고마움이 적혀 있습니다.'],
   'src':[S_182]},
 '장작평사':{'info':[('위치','하추자도 신양2리 해안 (지도 위치는 추정)'),('다른 이름','진작지'),('규모','몽돌 해안 약 300 m'),('지정','추자십경의 하나')],
   't':['신양2리 해안에 약 300 m에 걸쳐 몽돌이 쌓인 해안으로, 주민들은 진작지라고 부릅니다. 추자도의 아름다운 열 곳을 꼽은 추자십경 가운데 하나인 장작평사(長作平沙)가 바로 이곳입니다.',
        '지금은 이 일대에 해돋이 공원이 꾸며져 있어 아침 해를 보기 좋습니다. 파도가 몽돌 사이를 드나드는 소리를 들어 보세요.'],
   'src':[S_HA,S_GUN]},
 '돈대산':{'info':[('위치','하추자도'),('높이','해발 164 m (오픈스트리트맵 기준)')],
   't':['하추자도 가운데쯤 솟은 산입니다. 이 앱의 높이 값은 오픈스트리트맵에 등록된 값이며, 산에 대한 공식 소개 자료는 아직 찾지 못했습니다.'],
   'src':[S_OSM]},
 '추석산':{'info':[('위치','하추자도 예초리'),('높이','해발 155.7 m, 추자도 최고봉')],
   't':['하추자도 동쪽 예초리에 있는 산으로, 백과사전은 추자도에서 가장 높은 봉우리로 소개합니다.'],
   'src':[S_HA]},
 '전망바위':{'info':[('위치','하추자도 동쪽 해안')],
   't':['오픈스트리트맵에 전망 지점으로 등록된 곳입니다. 장소에 대한 공식 소개 자료는 아직 찾지 못했습니다.'],'src':[S_OSM]},
 '추자도등대':{'info':[('위치','오픈스트리트맵 기준 하추자도')],
   't':['한국관광공사 자료의 "추자도 등대"는 상추자도 영흥리에 있어, 이 지점과 같은 곳인지 아직 확인하지 못했습니다. 확인되면 설명을 보태겠습니다.'],'src':[S_OSM]},
 '신양항':{'ph':[('sinyanghang','신양항 여객선 대합실')],
   'info':[('위치','하추자도 신양리'),('코스','제주올레 18-2코스 시작점')],
   't':['하추자도의 관문으로, 하추자 올레 18-2코스가 여기서 시작해 졸복산과 대왕산 황금길로 이어집니다.',
        '항구 근처에는 추자도수협의 참조기 가공 단지가 있습니다. 추자도는 멸치잡이로 유명하고, 2008년부터 열린 추자도 참굴비축제는 2024년 제주 지역 최우수 축제로 뽑혔습니다.'],
   'src':[S_182,S_HA]},
 '예초리포구':{'info':[('위치','하추자도 동쪽 예초리')],
   't':['하추자도 동쪽 마을 예초리의 포구입니다. 예초리 해안에는 신대해수욕장이 있고, 마을 안쪽에는 추자도 최고봉인 추석산(155.7 m)이 솟아 있습니다.',
        '하추자도에는 1801년 신유박해 때 순교한 황사영과 정난주 사이에서 태어난 황경한의 묘소가 있습니다.'],
   'src':[S_HA]},
 '모진이몽돌해변':{'ph':[('mojini1','모진이몽돌해변 입구'),('mojini2','파도에 구르는 몽돌'),('mojini3','해변으로 내려가는 길')],
   'info':[('위치','하추자도 신양리, 추자면 신양4길 18'),('해변','모래 없이 몽돌로만 된 해변')],
   't':['모래 없이 동글동글한 돌로만 이루어진 해변입니다. 밀려오는 파도에 몽돌이 구르는 소리가 아름다워, 소리를 들으러 가기 좋은 곳입니다.',
        '물이 맑고 깨끗하며, 햇빛에 반사된 조약돌이 반짝이는 모습도 볼거리입니다.'],
   'src':['한국관광공사 「모진이몽돌해변」(원출처 비짓제주)',S_HA]},
 '봉글레산':{'info':[('위치','상추자도 대서리'),('높이','해발 85.5 m')],
   't':['상추자도 대서리 마을 뒤에 있는 산으로, 백과사전에는 봉골레산으로 적혀 있습니다. 북서풍을 막아 주는 이 산 아래 대서리 해안에 마을과 가게, 추자항이 모여 있습니다.'],
   'src':[S_SANG]},
 '순효각':{'info':[('위치','상추자도')],'t':['출처가 확인되는 소개 자료를 아직 찾지 못했습니다.'],'src':[S_OSM]},
 '제주최영장군사당':{'info':[('위치','상추자도 대서리, 추자면 대서4길 3-13'),('지정','제주특별자치도 기념물(1981년)'),('시대','고려 후기')],
   't':['고려 장수 최영의 은덕을 기리는 사당입니다. 1374년(공민왕 23) 최영은 전함 300여 척과 군사 2만 5000여 명을 이끌고 제주의 목호(牧胡) 반란을 진압하러 가던 길에, 거센 바람을 만나 추자도에 머물렀습니다.',
        '그때 최영이 주민들에게 그물로 고기 잡는 법을 가르쳐 주었고, 주민들이 그 은덕을 기려 사당을 세웠다고 합니다. 지금도 해마다 백중날과 음력 섣달 그믐에 제를 올려 풍어와 풍농을 빕니다.'],
   'src':['「최영 장군 사당」 - '+EK]},
 '추자처사각':{'info':[('위치','상추자도'),('지정','제주특별자치도 유형문화유산(1975년)'),('모신 분','조선 중기 처사 박인택')],
   't':['조선 중기에 추자도로 유배된 것으로 전하는 처사 박인택을 기리려고 후손들이 세운 사당입니다. 박인택은 추자도에 처음 들어온 태인 박씨의 시조가 되었습니다.',
        '맞배지붕에 바깥벽은 잡석으로 쌓았고, 바닷바람을 견디도록 정면 가운데 칸에만 판문을 달았습니다. 안쪽 감실에 위패를 모셨고 "영모재(永慕齋)" 현판이 걸려 있습니다.'],
   'src':['「추자 처사각」 - '+EK]},
 '상추자전망대':{'info':[('위치','상추자도')],'t':['오픈스트리트맵에 전망대로 등록된 곳입니다. 공식 소개 자료는 아직 찾지 못했습니다.'],'src':[S_OSM]},
 '용둠벙전망대':{'info':[('위치','상추자도 북서쪽 해안')],
   't':['상추자도 북서쪽 해안에는 "용둠벙"이라 불리는 해식지(파도에 깎여 움푹 팬 지형)가 있습니다. 하추자도 신양2리의 용둠벙과는 다른 곳입니다.'],
   'src':[S_SANG]},
 '상추자도항':{'ph':[('sangchuja1','상추자도항'),('sangchuja2','상추자도항의 추자도 조형물')],
   'info':[('위치','상추자도 대서리'),('코스','제주올레 18-1코스 시작점'),('뱃길','제주·목포·완도를 잇는 여객선 터미널')],
   't':['오목한 만에 자리한 추자도의 중심 항구로, 여객선 터미널이 있어 제주 본섬과 추자도를 잇는 뱃길의 중심입니다. 올레길을 따라가면 최영장군 사당과 나바론 절벽을 만납니다.',
        '수심이 깊고 밀물과 썰물의 차이가 작아 어선뿐 아니라 군함도 댈 수 있습니다.'],
   'src':['한국관광공사 「상추자항」',S_SANG]},
 '후포해변':{'info':[('위치','상추자도 북서쪽 해안'),('규모','몽돌 해변 약 120 m')],
   't':['상추자도 북서쪽 해안에 있는 길이 약 120 m의 몽돌 해변(후포해수욕장)입니다.'],
   'src':[S_SANG]},
}
COURSE=None
CSS='''
.px{grid-column:1/-1;margin-top:10px;min-width:0}
.px-row{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;padding-bottom:4px}
.px-fig{margin:0;flex:0 0 100%;scroll-snap-align:start;min-width:0}
.px-row.many .px-fig{flex-basis:86%}
.px-fig img{display:block;width:100%;aspect-ratio:3/2;object-fit:cover;border-radius:14px;background:var(--none)}
.px-fig figcaption,.pick .px-src,.px-src{color:var(--muted);font-size:12.5px;line-height:1.5;margin:5px 0 0}
.pick .px-t,.px-t{margin:10px 0 0;font-size:15px;line-height:1.65}
.pick .px-none,.px-none{margin:8px 0 0;color:var(--muted);font-size:13px;line-height:1.5}
.px-noph{display:grid;place-items:center;aspect-ratio:3/1;border-radius:14px;background:var(--none);color:var(--muted);font-size:13.5px}
.px-info{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 12px;margin:12px 0 0;font-size:14px;line-height:1.5}
.px-info dt{color:var(--muted);white-space:nowrap}.px-info dd{margin:0}
.plist small .px-b{color:var(--sea);font-weight:700}
'''
JS='''
(function(){
  var X=/*PX*/null,$=function(id){return document.getElementById(id)};
  function figs(a){return '<div class="px-row'+(a.length>1?' many':'')+'">'+a.map(function(p){return '<figure class="px-fig"><img loading="lazy" src="'+p.s+'" alt="'+p.a+'"><figcaption>'+p.a+' · 사진 '+X.c+'</figcaption></figure>'}).join('')+'</div>'}
  function body(e){var h=e.ph?figs(e.ph):'<div class="px-noph">이 장소의 사진은 준비 중입니다</div>';
    if(e.info)h+='<dl class="px-info">'+e.info.map(function(r){return '<dt>'+r[0]+'</dt><dd>'+r[1]+'</dd>'}).join('')+'</dl>';
    if(e.t)h+=e.t.map(function(x){return '<p class="px-t">'+x+'</p>'}).join('');
    if(e.src)h+='<p class="px-src">자료 출처: '+e.src.join(', ')+'</p>';return h}
  function pick(){var el=$('pick');if(!el||el.querySelector('.px'))return;var b=el.querySelector('b');if(!b||!b.firstChild)return;
    var e=X.p[b.firstChild.nodeValue];if(!e)return;var d=document.createElement('div');d.className='px';d.innerHTML=body(e);
    if(e.t){var op=el.querySelector(':scope > p');if(op)op.style.display='none'}el.appendChild(d)}
  function list(){var el=$('plist');if(!el)return;[].forEach.call(el.querySelectorAll('button'),function(b){var n=b.querySelector('span'),s=b.querySelector('small');
    if(!n||!s||s.querySelector('.px-b'))return;var e=X.p[n.textContent];if(e&&e.ph){var m=document.createElement('span');m.className='px-b';m.textContent=' · 사진';s.appendChild(m)}})}
  function all(){pick();list()}
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
    X={'c':KTO+'(공공누리 제1유형)','p':{n:_e(e) for n,e in PLACES.items()}}
    blk='<style id="px-css">'+CSS+'</style>\n<script id="px-js">'+JS.replace('/*PX*/null',json.dumps(X,ensure_ascii=False,separators=(',',':')))+'</script>\n'
    i=t.rindex('</body>') if '</body>' in t else len(t)
    return t[:i]+blk+t[i:]
