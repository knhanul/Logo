# Windows MSIX SVG 아이콘 PNG 묶음

icon-1은 파랑(#0273F5), icon-2는 주황(#FC6719)입니다. 두 SVG는 형태·viewBox(916×906)가 같고 선 색상과 원형 그라데이션 색상이 다릅니다. 중복 파일이 아닙니다.

각 폴더:
- source.svg: 원본 벡터
- Assets/: MSIX 배율 100/125/150/200/400, targetsize 기본·unplated·lightunplated
- PNG/: icon-44x44.png, icon-50x50.png, icon-150x150.png, icon-300x300.png 등 단독 파일

모든 크기는 원본 SVG를 각각 직접 렌더링했습니다. 비트맵 확대가 아니며 종횡비·색상·그라데이션을 유지했습니다. 캔버스 안쪽 약 8% 여백으로 중앙 배치했습니다. 원본의 투명 배경과 그라데이션 중앙 흰색을 유지했으며 배경 제거를 하지 않았습니다. 외부 SVG 리소스 요청은 차단했습니다.

## Manifest 연결
한 색상의 Assets 폴더를 선택하여 프로젝트 패키지 리소스에 포함하세요. 두 폴더를 같은 경로로 합치면 이름이 겹칩니다.
배율 없는 논리 경로를 manifest에 참조합니다. 실제 파일은 scale 한정자를 사용하며 빌드 리소스 시스템이 선택합니다.
- Properties/Logo: Assets\StoreLogo.png
- uap:VisualElements Square44x44Logo: Assets\Square44x44Logo.png
- uap:VisualElements Square150x150Logo: Assets\Square150x150Logo.png
- uap:DefaultTile Square71x71Logo/Wide310x150Logo/Square310x310Logo: 해당 이름의 Assets\*.png
- uap:SplashScreen Image: Assets\SplashScreen.png

300×300은 Square150x150Logo.scale-200.png입니다. scale-125는 50→63, 150→188, 310→388로 반올림했습니다. targetsize-44는 추가 크기입니다. 밝은/어두운 unplated에는 동일 색상 로고를 제공합니다.
타일·스플래시 사용 여부는 앱과 manifest에 따라 다르며 모든 파일이 필수는 아닙니다. 이 묶음은 PNG 리소스이며 실제 MSIX 패키징·Store 제출 검증은 수행하지 않았습니다.

규격 참고: https://learn.microsoft.com/en-us/windows/apps/design/iconography/app-icon-construction
