/* 신양愛소리 APK 전용: 앱을 열 때 깃허브에 올라온 최신 자료(data/live.json, 낮 동안 매시간 갱신)를 받아 화면에 반영한다.
   원본 화면 스크립트는 고치지 않는다. 새 자료를 기기에 저장한 뒤 화면을 한 번 다시 열면,
   원본 스크립트가 그 자료로 확률을 처음부터 다시 계산한다. 받지 못하면 마지막으로 받은 자료(없으면 내장 자료)를 쓴다. */
(function(){
  var URLS=['https://raw.githubusercontent.com/CyberJun777/CHUJACHUJA/main/data/live.json',
            'https://raw.githubusercontent.com/CyberJun777/CHUJACHUJA/HEAD/data/live.json'];
  var KEY='sinyang.live',G=window.__G;if(!G)return;
  var cur=G.D.live,lastTry=0,busy=false;
  function num(v){return typeof v==='number'&&isFinite(v)}
  function valid(L){try{
    if(!L||typeof L.fetched!=='string'||!/^\d{4}-\d\d-\d\d \d\d:\d\d$/.test(L.fetched))return false;
    if(typeof L.date!=='string'||!/^\d{8}$/.test(L.date))return false;
    if(!Array.isArray(L.stations)||!L.stations.length||!Array.isArray(L.schedule))return false;
    if(!L.stations.every(function(s){return typeof s.name==='string'&&typeof s.time==='string'&&num(s.wind)&&num(s.gust10)}))return false;
    if(!L.schedule.every(function(s){return typeof s.t==='string'&&typeof s.ship==='string'&&typeof s.frm==='string'&&typeof s.to==='string'}))return false;
    if(L.buoy&&!(typeof L.buoy.time==='string'&&num(L.buoy.wh)&&num(L.buoy.ws)&&num(L.buoy.gst)))return false;
    if(L.fc&&!(Array.isArray(L.fc)&&L.fc.every(function(f){return typeof f.fc==='string'&&typeof f.ef==='string'&&num(f.wh1)&&num(f.wh2)&&num(f.s1)&&num(f.s2)})))return false;
    return true}catch(e){return false}}
  function today(){return new Date(Date.now()+9*3600e3).toISOString().slice(0,10).replace(/-/g,'')}
  function when(L){return (+L.fetched.slice(5,7))+'월 '+(+L.fetched.slice(8,10))+'일 '+L.fetched.slice(11)}
  function banner(online){
    var stale=cur.date!==today(),txt='';
    if(stale)txt=(online?'오늘 자료가 아직 올라오지 않아 ':'새 자료를 받지 못해(인터넷 연결을 확인해 주세요) ')+when(cur)+'에 받은 자료를 보여 드립니다. 화면의 "지금"과 "오늘"은 그 날짜 기준이며 현재 바다 상태와 다를 수 있습니다.';
    ['view-home','view-ferry'].forEach(function(id){
      var v=document.getElementById(id);if(!v)return;
      var b=v.querySelector('.live-stale');
      if(!txt){if(b)b.remove();return}
      if(!b){b=document.createElement('div');b.className='live-stale';b.setAttribute('role','status');
        var a=v.querySelector('.top')||v.querySelector('header');a.parentNode.insertBefore(b,a.nextSibling)}
      b.textContent=txt});
  }
  function get(u){
    var c=window.AbortController?new AbortController():null,t=setTimeout(function(){c&&c.abort()},8000);
    return fetch(u+'?t='+Date.now(),{cache:'no-store',signal:c?c.signal:undefined})
      .then(function(r){clearTimeout(t);return r.ok?r.json():null}).catch(function(){clearTimeout(t);return null});
  }
  function check(){
    var now=Date.now();if(busy||now-lastTry<10*60e3)return;lastTry=now;busy=true;
    Promise.all(URLS.map(get)).then(function(rs){
      busy=false;
      var got=rs.filter(valid).sort(function(a,b){return a.fetched<b.fetched?1:-1})[0];
      if(got&&got.fetched>cur.fetched){
        var saved=false;
        try{localStorage.setItem(KEY,JSON.stringify(got));saved=localStorage.getItem(KEY)===JSON.stringify(got)}catch(e){}
        if(saved){location.reload();return}
      }
      banner(!!got);
    });
  }
  var n=document.getElementById('livenote');
  if(n)n.textContent=n.textContent.replace('이 화면은 스스로 새로 고쳐지지 않고, 자료를 다시 받아 올릴 때 바뀝니다.','앱을 열 때 인터넷에 연결되어 있으면 최신 자료를 새로 받아 옵니다. 자료는 오전 6시부터 오후 8시까지 한 시간마다 갱신됩니다.');
  banner(false);
  window.__liveCheck=check;
  document.addEventListener('visibilitychange',function(){if(!document.hidden)check()});
  check();
})();
