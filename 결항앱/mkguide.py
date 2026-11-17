# tpl.html(뱃길 앱) + map.json(실제 지도) → 결합 앱 틀 guide.tpl.html
import json
t=open('tpl.html',encoding='utf-8').read()
MAP=open('map.json',encoding='utf-8').read()
def rep(a,b):
    global t
    assert a in t,a[:60]; t=t.replace(a,b,1)
rep('<title>추자 뱃길 예보</title>','<title>신양愛소리</title>')
CSS='''
/* Guide shell: a main screen with two doors (sound map, ferry outlook); each opens a full view with a way back. */
[hidden]{display:none!important}
.top{display:flex;align-items:center;justify-content:space-between;gap:10px}
.top h1{font-size:21px;display:flex;flex-direction:column;line-height:1.25;color:var(--sea)}
.top h1 small{font-size:12px;font-weight:400;color:var(--muted);letter-spacing:.02em}
.view{display:flex;flex-direction:column;gap:14px}
.vt{font-size:20px;font-weight:700;color:var(--ink);margin:0}
.back{align-self:flex-start;color:var(--sea);font-weight:600;font-size:14px;padding:6px 10px 6px 0}
.door{display:flex;flex-direction:column;gap:12px;text-align:left;width:100%;background:var(--surface);border-radius:20px;padding:0;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.06)}
.door .pic{background:var(--deep);aspect-ratio:1000/520;overflow:hidden}
.door .pic svg{display:block;width:100%;height:100%}
.door .body{padding:0 18px 18px;display:flex;flex-direction:column;gap:6px}
.door .body.pad{padding-top:18px}
.door strong{font-size:19px;font-weight:700;display:flex;justify-content:space-between;align-items:center;gap:10px}
.door strong i{font-style:normal;color:var(--sea);font-size:22px;line-height:1}
.door p{margin:0;font-size:13.5px;color:var(--muted)}
.mini{display:grid;grid-template-columns:1fr auto;gap:2px 10px;align-items:baseline;padding:7px 0;border-top:1px solid var(--line);font-size:14px}
.mini small{display:block;color:var(--muted);font-size:12.5px}
.pc{font-family:var(--mono);font-weight:600;font-size:19px;font-variant-numeric:tabular-nums}
.heads{border-radius:12px;padding:10px 13px;font-size:13.5px;background:var(--sea-soft);color:var(--ink)}
.heads.warn{background:var(--warn-soft)} .heads b{font-weight:600}
.zoom{--n:4}
.zoom button{font-size:12.5px;padding:8px 2px}
.vtag{font-size:11px;font-weight:600;border-radius:999px;padding:1px 7px;background:var(--sea-soft);color:var(--sea);margin-left:6px;white-space:nowrap}
.pick p{grid-column:1/-1;margin:6px 0 0;font-size:13.5px}
.plist h3{font-size:12.5px;font-weight:600;color:var(--muted);margin:10px 0 2px}
.more{margin:0;padding-left:18px;font-size:13.5px;display:flex;flex-direction:column;gap:4px}
.map{position:relative;border-radius:16px;overflow:hidden;background:var(--deep)}
.map svg{display:block;width:100%;height:auto}
.mk{cursor:pointer} .mk:focus-visible{outline:2px solid var(--surface);outline-offset:2px}
.lg{display:flex;flex-wrap:wrap;gap:4px 14px;font-size:12.5px;color:var(--muted)}
.lg span{white-space:nowrap}.lg span::before{content:"";display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px;background:var(--c)}
.pick{display:grid;grid-template-columns:auto 1fr;gap:2px 12px;align-items:center}
.pick .no{grid-row:span 2;width:40px;height:40px;border-radius:50%;display:grid;place-items:center;color:var(--on);font-family:var(--mono);font-weight:600}
.pick b{font-size:17px}.pick span{font-size:13px;color:var(--muted)}
.plist{list-style:none;margin:0;padding:0}
.plist li{border-top:1px solid var(--line)}.plist li:first-child{border-top:0}
.plist button{display:grid;grid-template-columns:26px 1fr auto;gap:10px;align-items:center;width:100%;text-align:left;padding:9px 0;font-size:14px}
.plist i{width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font-style:normal;font-family:var(--mono);font-size:11.5px;font-weight:600;color:var(--on)}
.plist small{color:var(--muted);font-size:12.5px}
.plist button[aria-pressed="true"] span{font-weight:600}
.cta{width:100%;background:var(--sea);color:var(--surface);border-radius:999px;padding:12px 16px;font-size:15px;font-weight:600}
'''
rep('*{box-sizing:border-box}',CSS+'*{box-sizing:border-box}')
t=t.replace('--dot:#8FB2BC; --none:#DDE6E9;','--dot:#8FB2BC; --none:#DDE6E9; --deep:#BFDCE6; --land:#EEF3E4; --shore:#8DB3A0; --road:#FFFFFF; --roadc:#C9D3C4; --trail:#C98A3C; --on:#FFFFFF; --c1:#0B6E7F; --c2:#B4552D; --c3:#3E7D4B; --c4:#B8860B; --c5:#6A4C93; --warn-soft:#F6E7C8;')
assert t.count('--dot:#4A6C77; --none:#1D343D;')==2
t=t.replace('--dot:#4A6C77; --none:#1D343D;','--dot:#4A6C77; --none:#1D343D; --deep:#0E2C3A; --land:#23382F; --shore:#4E7565; --road:#51645B; --roadc:#1B2B25; --trail:#D9A35A; --on:#0B1A21; --c1:#4FC3D4; --c2:#F0946C; --c3:#7CCB8B; --c4:#E5B94A; --c5:#B79CE0; --warn-soft:#3F3213;')
HOME='''<div class="app">
 <div class="view" id="view-home">
  <div class="top">
    <h1>신양愛소리<small>추자도 신양2리 사운드스케이프 힐링 맵</small></h1>
    <p class="now" id="heroNow"></p>
    <svg class="wave" id="heroWave" viewBox="0 0 800 70" preserveAspectRatio="none" aria-hidden="true"></svg>
  </div>
  <div class="home-intro"><span class="section-kicker">추자도 신양2리</span><h2>바다의 소리를 따라<br>신양의 이야기를 만나보세요</h2><p>아래 메뉴에서 사운드스케이프, 운항·기상, 관광지와 이용 안내를 선택할 수 있습니다.</p></div>
  <div class="home-data" aria-hidden="true"><button class="door" id="door-map" tabindex="-1"><span class="pic" id="pic-map"></span><span class="body"><strong>사운드스케이프 맵</strong><p id="door-map-p"></p><span class="go">지도 열기</span></span></button><button class="door" id="door-ferry" tabindex="-1"><span class="body pad"><strong>운항 정보</strong><p>오늘 배가 뜰 확률과 앞으로 사흘의 결항 예보</p><span id="boatRows"></span><span class="heads" id="heads"></span><span class="go">운항 정보 보기</span></span></button></div>
  <div class="hint home-source">지도 © OpenStreetMap contributors. 운항 정보는 한국해양교통안전공단·기상청 자료로 계산합니다.</div>
 </div>
 <nav class="bottom-nav" aria-label="메인 메뉴"><button data-menu="map"><span class="menu-icon">◒</span><b>추자도<br>사운드스케이프</b></button><button data-menu="ferry"><span class="menu-icon">≋</span><b>운항정보 및<br>기상 정보</b></button><button data-menu="places"><span class="menu-icon">⌖</span><b>추자도<br>관광지</b></button><button data-menu="info"><span class="menu-icon">i</span><b>앱<br>이용안내</b></button></nav>

 <div class="view" id="view-info" hidden><button class="back" data-go="home">‹ 메인 화면</button><h2 class="vt">앱 이용안내</h2><section class="info-card"><span class="section-kicker">신양愛소리</span><h3>추자도의 소리와 정보를 한곳에서</h3><p>추자도 신양2리의 사운드스케이프와 관광지, 운항·기상 정보를 살펴볼 수 있습니다.</p></section><section class="info-card"><h3>메뉴 안내</h3><dl><dt>추자도 사운드스케이프</dt><dd>신양2리 명소와 추자도 관광지를 지도에서 둘러보고 파도 소리를 들어보세요.</dd><dt>운항정보 및 기상 정보</dt><dd>선박별 결항 확률과 파고·바람 조건, 앞으로 사흘의 예보를 확인합니다.</dd><dt>추자도 관광지</dt><dd>지도에 표시된 관광지 21곳과 장소 설명을 확인합니다.</dd></dl></section><p class="hint">운항 정보는 한국해양교통안전공단·기상청 자료를 바탕으로 계산합니다. 실제 탑승 전 최신 선사 공지를 확인하세요.</p></div>

 <div class="view" id="view-map" hidden>
  <button class="back" data-go="home">‹ 메인 화면</button>
  <h2 class="vt">사운드스케이프 맵</h2>
  <div class="seg zoom" id="zoom" role="group" aria-label="지도 범위">
    <button data-z="sy" aria-pressed="true">신양2리</button><button data-z="all" aria-pressed="false">전체</button><button data-z="ha" aria-pressed="false">하추자도</button><button data-z="sang" aria-pressed="false">상추자도</button>
  </div>
  <div class="map" id="map-full"></div>
  <div class="lg"><span style="--c:var(--c1)">항구</span><span style="--c:var(--c2)">전망·등대</span><span style="--c:var(--c3)">산</span><span style="--c:var(--c4)">해변</span><span style="--c:var(--c5)">유적</span><span style="--c:var(--trail)">탐방로</span></div>
  <section><div class="pick" id="pick"></div>
    <div class="sub" id="seaLine"></div>
    <button class="cta" id="listen" aria-pressed="false">파도 소리 듣기</button></section>
  <section>
    <h2 id="places">관광지</h2>
    <ul class="plist" id="plist"></ul>
    <h2>신양2리에서 더 만날 곳</h2>
    <ul class="more"><li>숭어 체험장</li><li>거북이 바위 쪽 해안과 용이 승천하려 나온 바위</li><li>바닷물 폭포 소리가 들리는 곳</li><li>마을 카페와 식당, 족욕 공간 (준비 중)</li></ul>
    <div class="hint">이장님 인터뷰에 나온 곳으로, 정확한 위치를 확인하면 지도에 올립니다. 점선 테두리 지점은 설명을 근거로 잡은 추정 위치입니다.</div>
    <div class="hint">지도와 그 밖의 관광지 위치는 오픈스트리트맵(© OpenStreetMap contributors)에 등록된 좌표입니다. 지점별 소리 정보는 다음 단계에서 추가합니다.</div>
  </section>
 </div>

 <div class="view" id="view-ferry" hidden>
  <button class="back" data-go="home">‹ 메인 화면</button>
  <header>
    <div><h2 class="vt">운항 정보</h2><div class="sub">추자도 여객선 결항 확률</div></div>
    <div class="sub" id="today"></div>
  </header>
'''
rep('''<div class="app">
  <header>
    <div><h1>추자 뱃길 예보</h1><div class="sub">추자도 여객선 결항 확률</div></div>
    <div class="sub" id="today"></div>
  </header>
''',HOME)
NAV=''' <nav class="tabs" aria-label="화면 이동">
  <button data-tab="home" aria-current="page"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 11.5 12 4l8 7.5V20a1 1 0 0 1-1 1h-4.5v-6h-5v6H5a1 1 0 0 1-1-1z"/></svg><span>홈</span></button>
  <button data-tab="map"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5a7 7 0 0 0-7 7c0 5 7 12 7 12s7-7 7-12a7 7 0 0 0-7-7zm0 9.6a2.6 2.6 0 1 1 0-5.2 2.6 2.6 0 0 1 0 5.2z"/></svg><span>소리 지도</span></button>
  <button data-tab="ferry"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.5 2h3v3H17l1 5 3 1.2-2.2 6.3c-.9.3-1.7.7-2.4 1.2-1.300-.9-2.900-.9-4.200 0-1.300-.9-2.900-.9-4.200 0-.7-.5-1.500-.9-2.400-1.200L3 11.200 6 10l1-5h3.500zM8.600 7l-.5 2.300L12 7.800l3.900 1.500-.5-2.300zM3 21c1.500 0 2.200-.5 3-1 .8.5 1.500 1 3 1s2.200-.5 3-1c.8.5 1.500 1 3 1s2.200-.5 3-1c.8.5 1.500 1 3 1v-1.800c-1 0-1.500-.4-2.200-.8l-.8-.5-.8.5c-.7.400-1.200.8-2.200.8s-1.500-.4-2.200-.8l-.8-.5-.8.5c-.7.400-1.200.8-2.200.8s-1.500-.4-2.200-.8L6 17.900l-.8.5c-.7.400-1.200.8-2.200.8z"/></svg><span>운항 정보</span></button>
 </nav>
'''
i=t.index('</div>\n\n<script>')
t=t[:i]+' </div>\n</div>\n\n<script>'+t[i+len('</div>\n\n<script>'):]
rep("  live();render();","  window.__G={D:D,prob:prob,render:render,state:state};\n  live();render();")
JS='''
<script>
(function(){
  var G=window.__G,D=G.D,M=/*MAP*/null,$=function(id){return document.getElementById(id)};
  var CC={'항구':1,'전망':2,'산':3,'해변':4,'유적':5},CN={'항구':'항구','전망':'전망·등대','산':'산','해변':'해변','유적':'유적'};
  var Z={sy:[520,440,300,270],all:[0,0,M.w,M.h],ha:[430,200,570,520],sang:[70,40,300,270]},zoom='sy',sel=M.pois.findIndex(function(p){return p.n==='대왕산'});if(sel<0)sel=0;
  function base(vb,marks){
    var k=vb[2]/1000;
    return '<svg viewBox="'+vb.join(' ')+'" role="img" aria-label="추자도 지도와 관광지 위치"><rect x="'+vb[0]+'" y="'+vb[1]+'" width="'+vb[2]+'" height="'+vb[3]+'" fill="var(--deep)"/>'+
      '<path d="'+M.land+'" fill="var(--land)" stroke="var(--shore)" stroke-width="'+(2*k)+'" stroke-linejoin="round"/>'+
      '<path d="'+M.pier+'" fill="none" stroke="var(--shore)" stroke-width="'+(3*k)+'"/>'+
      '<path d="'+M.trail+'" fill="none" stroke="var(--trail)" stroke-width="'+(2.2*k)+'" stroke-dasharray="'+(5*k)+' '+(4*k)+'" stroke-linecap="round"/>'+
      '<path d="'+M.road+'" fill="none" stroke="var(--roadc)" stroke-width="'+(5.5*k)+'" stroke-linecap="round" stroke-linejoin="round"/>'+
      '<path d="'+M.road+'" fill="none" stroke="var(--road)" stroke-width="'+(3.2*k)+'" stroke-linecap="round" stroke-linejoin="round"/>'+marks+'</svg>';
  }
  function marks(vb,labels){
    var k=vb[2]/1000,s='';
    if(labels){M.vil.forEach(function(v){s+='<text x="'+v.x+'" y="'+(v.y+34*k)+'" text-anchor="middle" font-size="'+(24*k)+'" fill="var(--muted)" font-weight="500">'+v.n+'</text>'});
      if(zoom==='all')s+='<text x="250" y="330" text-anchor="middle" font-size="30" font-weight="700" fill="var(--ink)" opacity=".75">상추자도</text><text x="560" y="520" text-anchor="middle" font-size="30" font-weight="700" fill="var(--ink)" opacity=".75">하추자도</text>'}
    M.pois.forEach(function(p,i){var on=i===sel&&labels,r=(on?24:labels?17:13)*k;
      s+='<g class="mk"'+(labels?' tabindex="0" role="button" aria-label="'+p.n+'"':'')+' data-i="'+i+'"><circle cx="'+p.x+'" cy="'+p.y+'" r="'+r+'" fill="var(--c'+CC[p.c]+')" stroke="var(--surface)" stroke-width="'+((on?5:3)*k)+'"'+(p.approx?' stroke-dasharray="'+(5*k)+' '+(3*k)+'"':'')+'/>'+
        (labels?'<text x="'+p.x+'" y="'+(p.y+7*k)+'" text-anchor="middle" font-size="'+((on?22:18)*k)+'" font-weight="700" fill="var(--on)" style="pointer-events:none">'+(i+1)+'</text>':'')+'</g>'});
    if(labels){var p=M.pois[sel],w=(p.n.length*26+28)*k,x=Math.min(Math.max(p.x-w/2,vb[0]+6*k),vb[0]+vb[2]-w-6*k),y=p.y-70*k<vb[1]?p.y+32*k:p.y-70*k;
      s+='<g style="pointer-events:none"><rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+(38*k)+'" rx="'+(19*k)+'" fill="var(--surface)" stroke="var(--line)" stroke-width="'+k+'"/><text x="'+(x+w/2)+'" y="'+(y+27*k)+'" text-anchor="middle" font-size="'+(24*k)+'" font-weight="600" fill="var(--ink)">'+p.n+'</text></g>'}
    return s;
  }
  function desc(p){return p.isl+'도 · '+CN[p.c]+(p.ele?' · 해발 '+Math.round(+p.ele)+' m':'')}
  function drawMap(){
    var vb=Z[zoom];$('map-full').innerHTML=base(vb,marks(vb,true));
    var p=M.pois[sel];$('pick').innerHTML='<div class="no" style="background:var(--c'+CC[p.c]+')">'+(sel+1)+'</div><b>'+p.n+(p.v?'<span class="vtag">'+p.v+'</span>':'')+'</b><span>'+desc(p)+(p.approx?' · 위치 추정':'')+'</span>'+(p.d?'<p>'+p.d+'</p>':'');
    var seen=false;$('plist').innerHTML=M.pois.map(function(q,i){var hd='';if(i===0&&q.v)hd='<h3>신양2리</h3>';if(!q.v&&!seen){seen=true;hd='<h3>추자도 다른 곳</h3>'}return '<li>'+hd+'<button data-i="'+i+'" aria-pressed="'+(i===sel)+'"><i style="background:var(--c'+CC[q.c]+')">'+(i+1)+'</i><span>'+q.n+'</span><small>'+(q.v||q.isl)+' · '+CN[q.c]+(q.approx?' · 추정':'')+'</small></button></li>'}).join('');
    [].forEach.call($('zoom').children,function(b){b.setAttribute('aria-pressed',String(b.dataset.z===zoom))});
  }
  function pick(e){var g=e.target.closest('[data-i]');if(!g)return;if(e.type==='keydown'){if(e.key!=='Enter'&&e.key!==' ')return;e.preventDefault()}
    sel=+g.dataset.i;var p=M.pois[sel];if(e.currentTarget.id==='plist'){zoom=p.v?'sy':p.isl==='상추자'?'sang':'ha';drawMap();$('zoom').scrollIntoView({block:'start',behavior:'smooth'})}else drawMap()}
  $('map-full').addEventListener('click',pick);$('map-full').addEventListener('keydown',pick);$('plist').addEventListener('click',pick);
  $('zoom').addEventListener('click',function(e){var b=e.target.closest('button');if(b){zoom=b.dataset.z;drawMap()}});

  function home(){
    $('pic-map').innerHTML=base([0,150,1000,520],marks([0,150,1000,520],false));
    $('door-map-p').textContent='신양2리 명소 '+M.pois.filter(function(p){return p.v}).length+'곳을 비롯해 실제 추자도 지도에서 관광지 '+M.pois.length+'곳을 둘러보세요.';
    var L=D.live,B=L.buoy,F=L.fc||[];
    (function(){var wh=B?B.wh:0.5,ws=B?B.ws:3,a=Math.max(3,Math.min(26,wh*10)),wl=Math.max(70,190-ws*9);
      function w(amp,len,y,ph){var d='M0 70 L0 '+y;for(var x=0;x<=1600;x+=8)d+=' L'+x+' '+(y+amp*Math.sin((x/len+ph)*6.283)).toFixed(1);return d+' L1600 70Z'}
      $('heroWave').innerHTML='<g class="wv"><path d="'+w(a,wl,36,0)+'" fill="rgba(255,255,255,.22)"/></g><g class="wv slow"><path d="'+w(a*.6,wl*1.6,44,.3)+'" fill="rgba(255,255,255,.3)"/></g>';
      $('heroNow').textContent=B?'지금 추자 바다는 파고 '+B.wh.toFixed(1)+' m, 바람 '+B.ws.toFixed(1)+' m/s':'지금 바다 관측값을 받지 못했습니다'})();
    var ships=D.ships.filter(function(s){return s.last>='2025'}),rows='',worst=null;
    ships.forEach(function(s){
      var p=B?G.prob(s.pts,B.wh,B.ws):null,left=L.schedule.filter(function(x){return x.ship===s.name&&x.se==='정상'});
      var ctl=L.schedule.filter(function(x){return x.ship===s.name&&x.se==='통제'}).length,off=!ctl&&!left.length;
      var txt=ctl?'오늘 '+ctl+'편 통제':left.length?'오늘 '+left.map(function(x){return x.t.slice(0,2)+':'+x.t.slice(2)+' '+x.frm+'발'}).join(', '):L.schedule.some(function(x){return x.ship===s.name&&x.why==='기상악화'})?'오늘은 기상 악화로 운항하지 않음':'오늘은 휴항';
      rows+='<span class="mini"><span>'+s.name+'<small>'+s.route+' · '+txt+'</small></span><span class="pc" style="color:var(--'+(p===null||off?'muted':p<15?'ok':p<40?'warn':'bad')+')">'+(p===null||off?'–':'결항 '+p+'%')+'</span></span>';
      F.forEach(function(f){var pp=G.prob(s.pts,(f.wh1+f.wh2)/2,(f.s1+f.s2)/2);if(!worst||pp>worst.p)worst={p:pp,f:f,s:s}});
    });
    $('boatRows').innerHTML=rows;var h=$('heads');
    if(!worst){h.className='heads';h.textContent='예보를 받지 못해 오늘 바다 상태 기준 확률만 보여 드립니다.'}
    else{var f=worst.f,when=(+f.ef.slice(4,6))+'월 '+(+f.ef.slice(6,8))+'일 '+(f.ef.slice(8,10)==='12'?'오후':'오전');
      if(worst.p>=20){h.className='heads warn';h.innerHTML='<b>'+when+'에는 배가 뜨지 않을 수 있어요.</b> 예보 파고 '+f.wh1.toFixed(1)+'~'+f.wh2.toFixed(1)+' m, '+worst.s.name+' 결항 확률 '+worst.p+'%'}
      else{h.className='heads';h.innerHTML='<b>앞으로 사흘은 뱃길이 순조로울 전망입니다.</b> 가장 높은 결항 확률 '+worst.p+'%('+when+')'}}
    $('seaLine').textContent=B?'지금 추자 바다는 파고 '+B.wh.toFixed(1)+' m, 바람 '+B.ws.toFixed(1)+' m/s입니다. '+(B.wh<1?'파도 소리가 잔잔한 시간이에요.':B.wh<2?'파도 소리가 또렷한 시간이에요.':'파도가 거칩니다. 해안 가까이는 피하세요.'):'';
  }

  var V=['home','map','ferry'];
  function show(){var v=location.hash.slice(1);if(V.indexOf(v)<0)v='home';
    V.forEach(function(k){$('view-'+k).hidden=k!==v});if(v==='ferry')G.render();if(v==='map')drawMap();$('view-info').hidden=true;window.__tab&&window.__tab(v);window.scrollTo(0,cur==='places'&&v==='map'?$('places').getBoundingClientRect().top+window.pageYOffset-16:0)}
  function go(v){location.hash=v;show()}
  $('door-map').onclick=function(){go('map')};$('door-ferry').onclick=function(){go('ferry')};
  [].forEach.call(document.querySelectorAll('.back'),function(b){b.onclick=function(){go('home')}});
  // 하단 메뉴 4개 (Manus 개선본 구조). 관광지 탭은 지도 화면의 목록으로, 이용안내는 별도 화면.
  var cur='home';
  window.__tab=function(v){if(v!=='map'||cur!=='places')cur=v;[].forEach.call(document.querySelectorAll('.bottom-nav button'),function(b){if(b.dataset.menu===cur)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current')})};
  [].forEach.call(document.querySelectorAll('.bottom-nav button'),function(b){b.onclick=function(){var m=b.dataset.menu;
    if(m==='info'){V.forEach(function(k){$('view-'+k).hidden=true});$('view-info').hidden=false;cur='info';window.__tab('info');window.scrollTo(0,0);return}
    cur=m;go(m==='places'?'map':m)}});
  addEventListener('hashchange',show);

  var ac=null,gain=null,on=false;
  $('listen').onclick=function(){
    try{
      if(!ac){ac=new (window.AudioContext||window.webkitAudioContext)();
        var n=ac.sampleRate*4,buf=ac.createBuffer(1,n,ac.sampleRate),d=buf.getChannelData(0),l=0;
        for(var i=0;i<n;i++){l=0.985*l+0.015*(Math.random()*2-1);d[i]=l*9}
        var src=ac.createBufferSource();src.buffer=buf;src.loop=true;
        var lp=ac.createBiquadFilter();lp.type='lowpass';lp.frequency.value=900;
        gain=ac.createGain();gain.gain.value=0;
        var lfo=ac.createOscillator(),lg=ac.createGain();lfo.frequency.value=0.11;lg.gain.value=0.22;
        var swell=ac.createGain();swell.gain.value=0.3;lfo.connect(lg);lg.connect(swell.gain);
        src.connect(lp);lp.connect(swell);swell.connect(gain);gain.connect(ac.destination);src.start();lfo.start()}
      on=!on;ac.resume();gain.gain.linearRampToValueAtTime(on?1:0,ac.currentTime+0.8);
      this.textContent=on?'파도 소리 끄기':'파도 소리 듣기';this.setAttribute('aria-pressed',String(on));
    }catch(e){this.textContent='이 기기에서는 소리를 재생할 수 없습니다'}
  };
  home();drawMap();show();
})();
</script>
'''.replace('/*MAP*/null',MAP)
t=t.rstrip()+'\n'+JS
import skin; t=skin.apply(t)
import places_extra; t=places_extra.apply(t)  # 관광지 사진·자료 덧붙임
open('guide.tpl.html','w',encoding='utf-8').write(t)
print('ok',len(t))
