from pathlib import Path
from PIL import Image, ImageDraw
from defusedxml import ElementTree as ET
import xml.etree.ElementTree as X
import cairosvg, io, csv, zipfile, hashlib, math, re
root=Path('/workspace/msix-svg-icons-20261108')
ns='http://www.w3.org/2000/svg'; X.register_namespace('',ns)
bases={'Square44x44Logo':(44,44),'StoreLogo':(50,50),'Square71x71Logo':(71,71),'Square150x150Logo':(150,150),'Square310x310Logo':(310,310),'Wide310x150Logo':(310,150),'SplashScreen':(620,300)}
rows=[];sources=[]
def deny(*args,**kwargs): raise ValueError('External resources forbidden')
def render(data,w,h):
 node=ET.fromstring(data); vb=list(map(float,node.attrib['viewBox'].split())); sw,sh=vb[2:]
 factor=min(.84*w/sw,.84*h/sh); rw,rh=sw*factor,sh*factor
 node.set('x',str((w-rw)/2));node.set('y',str((h-rh)/2));node.set('width',str(rw));node.set('height',str(rh))
 outer=X.Element('{'+ns+'}svg',width=str(w),height=str(h),viewBox=f'0 0 {w} {h}');outer.append(node)
 raw=cairosvg.surface.PNGSurface.convert(bytestring=X.tostring(outer),url_fetcher=deny)
 return Image.open(io.BytesIO(raw)).convert('RGBA')
def save(data,folder,name,w,h):
 p=root/folder/name;p.parent.mkdir(parents=True,exist_ok=True);render(data,w,h).save(p,optimize=True);rows.append((str(p.relative_to(root)),w,h,'RGBA'))
for i in (1,2):
 data=Path(f'/workspace/msix-svg-input-20261108/icon-{i}.svg').read_bytes();sources.append(data)
 node=ET.fromstring(data)
 for el in node.iter():
  assert el.tag.split('}')[-1] in ('svg','defs','radialGradient','stop','path','circle'),el.tag
  for k,v in el.attrib.items():
   assert not k.lower().startswith('on') and not k.endswith('href')
   for u in re.findall(r'url\((.*?)\)',v):assert u.startswith('#')
 folder=f'icon-{i}';(root/folder).mkdir(exist_ok=True);(root/folder/'source.svg').write_bytes(data)
 for name,(bw,bh) in bases.items():
  for scale in (100,125,150,200,400):
   w,h=math.floor(bw*scale/100+.5),math.floor(bh*scale/100+.5)
   save(data,f'{folder}/Assets',f'{name}.scale-{scale}.png',w,h)
 for size in (16,20,24,30,32,36,40,44,48,60,64,72,80,96,256):
  for suffix in ('','_altform-unplated','_altform-lightunplated'):
   save(data,f'{folder}/Assets',f'Square44x44Logo.targetsize-{size}{suffix}.png',size,size)
 for size in (16,24,32,44,48,50,64,128,150,256,300,310,512):
  save(data,f'{folder}/PNG',f'icon-{size}x{size}.png',size,size)
 with (root/folder/'README-KO.md').open('w') as f:
  f.write(f'icon-{i}: '+('파랑 #0273F5' if i==1 else '주황 #FC6719')+'\n원본 SVG와 동일한 형태·색·그라데이션·투명 배경입니다.\nAssets는 MSIX 배율/targetsize 세트, PNG는 크기별 단독 파일입니다.\n')
with (root/'asset-dimensions.csv').open('w') as f:
 wr=csv.writer(f);wr.writerow(('file','width','height','mode'));wr.writerows(rows)
(root/'README-KO.md').write_text('''# Windows MSIX SVG 아이콘 PNG 묶음

icon-1은 파랑(#0273F5), icon-2는 주황(#FC6719)입니다. 두 SVG는 형태·viewBox(916×906)가 같고 선 색상과 원형 그라데이션 색상이 다릅니다. 중복 파일이 아닙니다.

각 폴더:
- source.svg: 원본 벡터
- Assets/: MSIX 배율 100/125/150/200/400, targetsize 기본·unplated·lightunplated
- PNG/: icon-44x44.png, icon-50x50.png, icon-150x150.png, icon-300x300.png 등 단독 파일

모든 크기는 원본 SVG를 각각 직접 렌더링했습니다. 비트맵 확대가 아니며 종횡비·색상·그라데이션을 유지했습니다. 캔버스 안쪽 약 8% 여백으로 중앙 배치했습니다. 원본의 투명 배경과 그라데이션 중앙 흰색을 유지했으며 배경 제거를 하지 않았습니다. 외부 SVG 리소스 요청은 차단했습니다.

## Manifest 연결
한 색상의 Assets 폴더를 선택하여 프로젝트 패키지 리소스에 포함하세요. 두 폴더를 같은 경로로 합치면 이름이 겹칩니다.
배율 없는 논리 경로를 manifest에 참조합니다. 실제 파일은 scale 한정자를 사용하며 빌드 리소스 시스템이 선택합니다.
- Properties/Logo: Assets\\StoreLogo.png
- uap:VisualElements Square44x44Logo: Assets\\Square44x44Logo.png
- uap:VisualElements Square150x150Logo: Assets\\Square150x150Logo.png
- uap:DefaultTile Square71x71Logo/Wide310x150Logo/Square310x310Logo: 해당 이름의 Assets\\*.png
- uap:SplashScreen Image: Assets\\SplashScreen.png

300×300은 Square150x150Logo.scale-200.png입니다. scale-125는 50→63, 150→188, 310→388로 반올림했습니다. targetsize-44는 추가 크기입니다. 밝은/어두운 unplated에는 동일 색상 로고를 제공합니다.
타일·스플래시 사용 여부는 앱과 manifest에 따라 다르며 모든 파일이 필수는 아닙니다. 이 묶음은 PNG 리소스이며 실제 MSIX 패키징·Store 제출 검증은 수행하지 않았습니다.

규격 참고: https://learn.microsoft.com/en-us/windows/apps/design/iconography/app-icon-construction
''')
# Actual-size previews, no PNG rescaling.
preview=Image.new('RGBA',(1140,740),'#eeeeee');d=ImageDraw.Draw(preview)
for row,data in enumerate(sources):
 for col,bg in enumerate(('checker','white','dark')):
  x,y=col*380+10,row*365+10
  d.text((x,y),f'icon-{row+1} / {bg} / 256, 44, 50 px',fill='black')
  y+=24;d.rectangle((x,y,x+360,y+320),fill={'checker':'#ddd','white':'white','dark':'#202124'}[bg])
  if bg=='checker':
   for yy in range(y,y+320,10):
    for xx in range(x,x+360,10):
     if ((yy-y)//10+(xx-x)//10)%2:d.rectangle((xx,yy,xx+9,yy+9),fill='#aaa')
  preview.alpha_composite(render(data,256,256),(x+8,y+30))
  preview.alpha_composite(render(data,44,44),(x+285,y+75));preview.alpha_composite(render(data,50,50),(x+282,y+150))
preview.save('/workspace/msix-svg-icons-preview-20261108.png');preview.save(root/'preview.png')
for rel,w,h,mode in rows:
 with Image.open(root/rel) as im:
  im.load();assert im.size==(w,h) and im.mode==mode,rel
with zipfile.ZipFile('/workspace/msix-svg-icons-20261108.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(root))
with zipfile.ZipFile('/workspace/msix-svg-icons-20261108.zip') as z:
 assert z.testzip() is None
 assert len([n for n in z.namelist() if n.endswith('.png')])==len(rows)+1
print('Identical sources:',sources[0]==sources[1]);print('PNG assets:',len(rows),'per icon:',len(rows)//2)
print('ZIP bytes:',Path('/workspace/msix-svg-icons-20261108.zip').stat().st_size)
