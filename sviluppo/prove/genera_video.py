"""Crea vacche.y4m, la "fotocamera finta" per le prove automatiche.
Uso: python genera_video.py dorso_A.png dorso_B.png
Sequenza: vacca A per 16 s (registrazione), vacca B per 10 s, di nuovo A per 10 s.
I dorsi di prova vanno ritagliati da immagini di Frisone viste dall'alto: per esempio
le anteprime pubbliche di github.com/dataset-ninja/cows2021 (cartella visualizations).
Richiede Pillow e ffmpeg."""
import sys, os, math, subprocess, tempfile
from PIL import Image, ImageEnhance, ImageDraw
A=Image.open(sys.argv[1]).convert('RGB'); B=Image.open(sys.argv[2]).convert('RGB')
W,H=720,1280; gw=int(W*0.88)
tmp=tempfile.mkdtemp()
def frame(src,t):
    bg=Image.new('RGB',(W,H),(70,66,60)); d=ImageDraw.Draw(bg)
    for k in range(0,H,90): d.line([0,k,W,k+40],fill=(60,56,50),width=8)
    s=1.15+0.06*math.sin(t*0.9); w=int(gw*s); h=int(w*src.height/src.width)
    im=src.resize((w,h)).rotate(4*math.sin(t*0.7),resample=Image.BILINEAR)
    im=ImageEnhance.Brightness(im).enhance(1+0.12*math.sin(t*1.7))
    cx=W//2+int(25*math.sin(t*0.5)); cy=H//2+int(18*math.cos(t*0.6))
    bg.paste(im,(cx-w//2,cy-h//2)); return bg
n=0
for src,secs in [(A,16),(B,10),(A,10)]:
    for i in range(secs*10): frame(src,n/10).save(f'{tmp}/{n:04d}.png'); n+=1
out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'vacche.y4m')
subprocess.run(['ffmpeg','-loglevel','error','-y','-framerate','10','-i',f'{tmp}/%04d.png','-pix_fmt','yuv420p',out],check=True)
print('creato',out)
