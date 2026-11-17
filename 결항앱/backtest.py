# 앱 확률(최근접 이웃) 검증: 과거 날짜를 하나씩 빼고 나머지로 예측해 실제 통제 여부와 비교
import json
d=json.load(open('data.json',encoding='utf-8'))
RW,RS=0.3,1.5
def prob(pts,w,s):
    sc=sorted(((( p[0]-w)/RW)**2+((p[1]-s)/RS)**2,p[2]) for p in pts)
    n=[h for q,h in sc if q<=1]
    if len(n)<25: n=[h for q,h in sc[:25]]
    return sum(n)/len(n)
if __name__=='__main__':
    for s in d['ships']:
        P=s['pts']; res=[]
        for i,p in enumerate(P): res.append((prob(P[:i]+P[i+1:],p[0],p[1]),p[2]))
        n=len(res); hit=sum(h for _,h in res)
        brier=sum((q-h)**2 for q,h in res)/n; base=hit/n; bref=base*(1-base)
        tp=sum(1 for q,h in res if q>=.5 and h); fp=sum(1 for q,h in res if q>=.5 and not h); fn=sum(1 for q,h in res if q<.5 and h); tn=n-tp-fp-fn
        print(f"\n{s['name']}: {n}일, 실제 통제 {hit}일({base*100:.1f}%) | 50% 기준 맞힌 날 {(tp+tn)/n*100:.1f}% | 통제 예측 {tp+fp}일 중 실제 {tp} | 놓친 통제 {fn}일 | 헛경보 {fp}일 | Brier {brier:.3f} (기준 {bref:.3f})")
        for lo,hi in [(0,.05),(.05,.15),(.15,.4),(.4,.7),(.7,1.01)]:
            b=[(q,h) for q,h in res if lo<=q<hi]
            if b: print(f"  앱 확률 {int(lo*100):>2}~{min(100,int(hi*100)):>3}%: {len(b):>4}일, 평균 예측 {sum(q for q,_ in b)/len(b)*100:5.1f}% / 실제 통제 {sum(h for _,h in b)/len(b)*100:5.1f}%")
        miss=sorted([(q,P[i]) for i,(q,h) in enumerate(res) if h and q<.15])[:5]
        print('  낮게 봤는데 통제된 날 예:',[(round(q*100),p[0],p[1]) for q,p in miss], '총',sum(1 for q,h in res if h and q<.15))
