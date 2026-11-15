from PIL import Image,ImageDraw
from pathlib import Path
import numpy as np, math, csv, zipfile, shutil
root=Path('/workspace/msix-icon-assets-20261107')
src=Image.open('/workspace/msix-icon-input/source.png').convert('RGBA')
shutil.copy('/workspace/msix-icon-input/source.png',root/'source-original.png')
a=np.array(src).astype(float); rgb=a[:,:,:3]; mn=rgb.min(2)
# Recover edge coverage from nearby fully coloured pixels on the original white matte.
out=a.copy(); out[:,:,3]=np.where(mn==255,0,255)
ys,xs=np.where((mn>100)&(mn<255))
for y,x in zip(ys,xs):
 y0,y1=max(0,y-5),min(src.height,y+6); x0,x1=max(0,x-5),min(src.width,x+6)
 yy,xx=np.where(mn[y0:y1,x0:x1]<100)
 if len(yy):
  k=np.argmin((yy+y0-y)**2+(xx+x0-x)**2); base=rgb[yy[k]+y0,xx[k]+x0].min()
  alpha=min(1,(255-mn[y,x])/(255-base))
  out[y,x,:3]=np.clip((rgb[y,x]-255*(1-alpha))/alpha,0,255);out[y,x,3]=round(alpha*255)
 else:
  alpha=(255-mn[y,x])/(255-26)
  out[y,x,:3]=np.clip((rgb[y,x]-255*(1-alpha))/alpha,0,255);out[y,x,3]=round(alpha*255)
transparent=Image.fromarray(out.astype('uint8'),'RGBA')
bbox=transparent.getbbox(); transparent=transparent.crop(bbox); white=src.crop(bbox)
rows=[]
def save(im,path,w,h):
 path.parent.mkdir(parents=True,exist_ok=True);im.save(path,optimize=True);rows.append((str(path.relative_to(root)),w,h,'RGBA'))
def render(w,h,bg):
 logo=transparent if bg=='transparent' else white
 # 8% breathing room on each side, aspect ratio retained.
 fit=min(w*.84/logo.width,h*.84/logo.height)
 size=(max(1,round(logo.width*fit)),max(1,round(logo.height*fit)))
 tile=Image.new('RGBA',(w,h),(255,255,255,0) if bg=='transparent' else (255,255,255,255))
 small=logo.resize(size,Image.Resampling.LANCZOS);tile.alpha_composite(small,((w-size[0])//2,(h-size[1])//2));return tile
bases={'Square44x44Logo':(44,44),'StoreLogo':(50,50),'Square71x71Logo':(71,71),'Square150x150Logo':(150,150),'Square310x310Logo':(310,310),'Wide310x150Logo':(310,150),'SplashScreen':(620,300)}
for bg,folder in [('transparent','Assets'),('white','WhiteBackground/Assets')]:
 for name,(bw,bh) in bases.items():
  for scale in (100,125,150,200,400):
   w,h=math.floor(bw*scale/100+.5),math.floor(bh*scale/100+.5)
   save(render(w,h,bg),root/folder/f'{name}.scale-{scale}.png',w,h)
 for size in (16,20,24,30,32,36,40,44,48,60,64,72,80,96,256):
  for suffix in ('','_altform-unplated','_altform-lightunplated'):
   save(render(size,size,bg),root/folder/f'Square44x44Logo.targetsize-{size}{suffix}.png',size,size)
 for size in (16,20,24,30,32,36,40,44,48,50,60,64,71,72,80,96,128,150,256,300,310,512,600,1024):
  save(render(size,size,bg),root/'PNG'/bg/f'icon-{size}x{size}.png',size,size)
with (root/'asset-dimensions.csv').open('w') as f:
 wr=csv.writer(f);wr.writerow(['file','width','height','mode']);wr.writerows(rows)
readme='''# Windows MSIX PNG 아이콘\n\n- Assets/: 투명 배경 기본 세트. WhiteBackground/Assets/: 원본 흰 배경 유지 대안. 두 세트를 섞지 말고 하나를 선택하세요.\n- PNG/transparent, PNG/white: 크기별 단독 파일(44, 50, 150, 300, 310, 512 등).\n- 원본은 180×226 RGB(불투명 흰 배경) 비트맵입니다. 로고 비율·그라데이션·점 무늬를 유지해 중앙 배치했습니다. 가장자리 여백은 약 8%입니다.\n- 투명 버전은 흰 배경과 흰 점 무늬를 함께 투명한 녹아웃으로 처리하고 흰 배경에 섞인 가장자리 색을 보정했습니다. 원본에서 알파를 복원한 추정치이므로 원본 외관을 엄밀히 유지하려면 흰 배경 버전을 쓰세요.\n- 확대 PNG는 보간한 것이며 벡터가 아닙니다. 큰 크기에서는 원본 해상도 한계가 있습니다.\n\n## 패키지 연결\nAssets 폴더를 프로젝트에 포함하고 패키지 리소스로 빌드하세요. Manifest에는 배율 없는 논리 파일명을 참조합니다(실제 파일은 .scale-100 등 배율 한정자 포함).\n- Properties/Logo: Assets\\StoreLogo.png\n- uap:VisualElements의 Square44x44Logo: Assets\\Square44x44Logo.png\n- uap:VisualElements의 Square150x150Logo: Assets\\Square150x150Logo.png\n- uap:DefaultTile의 Square71x71Logo, Wide310x150Logo, Square310x310Logo: 같은 이름의 Assets\\*.png\n- uap:SplashScreen Image: Assets\\SplashScreen.png\n\n300×300은 Square150x150Logo.scale-200.png입니다. 125%의 150→188, 50→63, 310→388은 Microsoft 표에 맞게 반올림했습니다.\nTarget-size에는 기본·unplated·lightunplated 파일을 제공합니다. 44px은 추가 선택 크기입니다. 밝은/어두운 테마 모두 같은 컬러 로고를 사용합니다.\n타일·스플래시는 앱/manifest에 따라 선택 사항입니다. 모든 파일을 반드시 사용해야 하는 것은 아니며 이 묶음은 Store 등록용 스크린샷이나 MSIX 패키지 자체가 아닙니다. 실제 빌드·Store 검증은 별도로 진행하세요.\n\n공식 규격 참고: https://learn.microsoft.com/en-us/windows/apps/design/iconography/app-icon-construction\n'''
(root/'README-KO.md').write_text(readme)
# Contact sheet: actual 44/50/150/300px icons, shown without resampling.
canvas=Image.new('RGBA',(1160,790),'#eeeeee');d=ImageDraw.Draw(canvas)
for col,bg in enumerate(('checker','white','dark')):
 x=col*385+10;d.text((x,10),bg,fill='black')
 for y,size in ((45,44),(125,50),(220,150),(435,300)):
  w=350;h=max(size+20,65)
  color='#ffffff' if bg=='white' else '#202124' if bg=='dark' else '#ddd'
  d.rectangle((x,y,x+w,y+h),fill=color)
  if bg=='checker':
   for yy in range(y,y+h,12):
    for xx in range(x,x+w,12):
     if ((xx-x)//12+(yy-y)//12)%2:d.rectangle((xx,yy,min(xx+11,x+w),min(yy+11,y+h)),fill='#aaa')
  canvas.alpha_composite(render(size,size,'transparent'),(x+20,y+10))
  d.text((x+5,y-14),f'{size} x {size}',fill='black')
canvas.save('/workspace/msix-icon-preview.png');canvas.save(root/'preview.png')
# Verify all deliverable PNGs are decodable RGBA and dimensions match inventory.
for rel,w,h,mode in rows:
 with Image.open(root/rel) as im:
  im.load();assert im.size==(w,h) and im.mode==mode,rel
with zipfile.ZipFile('/workspace/msix-icon-assets.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in root.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(root))
with zipfile.ZipFile('/workspace/msix-icon-assets.zip') as z:assert z.testzip() is None
print('Source',src.size,'crop',bbox,'Generated asset PNGs',len(rows))
print('ZIP bytes',Path('/workspace/msix-icon-assets.zip').stat().st_size)
