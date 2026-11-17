from PIL import Image, ImageDraw
import math, os
S=1024
def make(round_bg):
    im=Image.new('RGBA',(S,S),(0,0,0,0)); d=ImageDraw.Draw(im)
    if round_bg: d.rounded_rectangle([0,0,S-1,S-1],radius=230,fill='#2563EB')
    else: d.rectangle([0,0,S,S],fill='#2563EB')
    # three wave lines, like sound over sea
    for i,(y,amp,w,a) in enumerate([(380,70,54,255),(520,70,54,200),(660,70,54,140)]):
        pts=[(x, y+amp*math.sin((x-230)/564*2*math.pi*1.5+i*0.9)) for x in range(230,795,3)]
        col=(255,255,255,a)
        layer=Image.new('RGBA',(S,S),(0,0,0,0)); ld=ImageDraw.Draw(layer)
        for p in pts: ld.ellipse([p[0]-w/2,p[1]-w/2,p[0]+w/2,p[1]+w/2],fill=col)
        im.alpha_composite(layer)
    return im
im=make(True)
for name,px in [('mdpi',48),('hdpi',72),('xhdpi',96),('xxhdpi',144),('xxxhdpi',192)]:
    os.makedirs(f'app/res/mipmap-{name}',exist_ok=True)
    im.resize((px,px),Image.LANCZOS).save(f'app/res/mipmap-{name}/ic_launcher.png')
im.resize((512,512),Image.LANCZOS).save('icon_preview.png')
