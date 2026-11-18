# 스킨: Manus 개선본(2026-11-17, 신양애소리_개선_시연용.apk)의 디자인을 그대로 입힌다.
#  skin_base.css   Manus가 바탕으로 삼은 이전 스킨
#  hanja_font.css  愛 한 글자용 내장 글꼴
#  manus_polish.css Manus의 덮어쓰기 CSS (원문 그대로, 고치지 말 것)
# apply(html)이 색 토큰 값을 바꾸고 위 CSS를 </style> 앞에 붙인다. 원본 JS·데이터·id는 건드리지 않는다.
import re,os
HERE=os.path.dirname(os.path.abspath(__file__))
def rd(n): return open(os.path.join(HERE,n),encoding='utf-8').read()
L=dict(bg='#F1F4F9',surface='#FFFFFF',ink='#111827',muted='#6B7280',line='#E6E9EF',sea='#2563EB',
 ok='#16A34A',warn='#D97706',bad='#DC2626',dot='#A9BEDF',none='#E5E9F0',deep='#CFE0FB',land='#F7F8F3',
 shore='#9DB4D6',road='#FFFFFF',roadc='#D5DAE2',trail='#E08A3C',on='#FFFFFF',c1='#2563EB',c2='#E0562F',
 c3='#2F9E62',c4='#D99A0B',c5='#7C5CD6')
L['sea-soft']='#E8F0FE'; L['warn-soft']='#FEF3C7'
D=dict(bg='#0B1020',surface='#151B2E',ink='#EEF2FF',muted='#98A2B8',line='#27304A',sea='#6B98FF',
 ok='#4ADE80',warn='#FBBF24',bad='#F87171',dot='#4B5F8A',none='#1E2740',deep='#0F1D3D',land='#222B3A',
 shore='#46587C',road='#4A566E',roadc='#1A2233',trail='#E6A45C',on='#0B1020',c1='#6B98FF',c2='#FF9670',
 c3='#6FD39A',c4='#F0C24A',c5='#B7A0F5')
D['sea-soft']='#1B2A52'; D['warn-soft']='#3D3112'
# Manus 개선본에 없던 보완: 지금 있는 화면의 탭만 강조(인수인계 문서의 '향후 개선 후보'), 메인 화면 숨김 카드는 누를 수 없게
EXTRA='''
/* Additions on top of the Manus pass: highlight the tab of the current screen instead of always the first one. */
.bottom-nav button:first-child{background:transparent;color:var(--muted)}
.bottom-nav button[aria-current="page"],.bottom-nav button:focus-visible{background:var(--sea-soft);color:var(--sea)}
.home-data{pointer-events:none}
'''
SOLO='.app>header{padding:16px 16px 0}.app>section,.app>.seg,.app>.notice{margin:0 16px}.app{gap:14px;padding-bottom:26px}\n'
FONT='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gothic+A1:wght@400;500;600;700;800&display=swap">\n'
def apply(h):
    i=h.index(':root{'); j=h.index('*{box-sizing')
    head=h[i:j]
    parts=re.split(r'(?=@media \(prefers-color-scheme)',head,1)
    def sw(s,m):
        for k,v in m.items(): s=re.sub(r'--'+k+r':#[0-9A-Fa-f]{3,8}','--'+k+':'+v,s)
        return s
    head=sw(parts[0],L)+sw(parts[1],D)
    h=h[:i]+head+h[j:]
    css=rd('skin_base.css')+rd('hanja_font.css')+rd('manus_polish.css')+EXTRA+('' if 'class="view"' in h else SOLO)
    k=h.rindex('</style>')
    h=h[:k]+css+h[k:]
    i=h.index('<style')
    h=h[:i]+FONT+h[i:]
    # 2026-11-18 도양님 "흰색 배경에 파란색으로, 전체 조정": 휴대폰 다크 모드여도 항상 밝은 테마로 고정
    h=re.sub(r'prefers-color-scheme:\s*dark','prefers-color-scheme: light-only-off',h)
    h=h.replace(':root{',':root{color-scheme:light;',1)
    if '<meta name="color-scheme"' not in h:
        h=h.replace('<style','<meta name="color-scheme" content="light">\n<style',1)
    return h
