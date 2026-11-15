# Windows MSIX PNG 아이콘

- Assets/: 투명 배경 기본 세트. WhiteBackground/Assets/: 원본 흰 배경 유지 대안. 두 세트를 섞지 말고 하나를 선택하세요.
- PNG/transparent, PNG/white: 크기별 단독 파일(44, 50, 150, 300, 310, 512 등).
- 원본은 180×226 RGB(불투명 흰 배경) 비트맵입니다. 로고 비율·그라데이션·점 무늬를 유지해 중앙 배치했습니다. 가장자리 여백은 약 8%입니다.
- 투명 버전은 흰 배경과 흰 점 무늬를 함께 투명한 녹아웃으로 처리하고 흰 배경에 섞인 가장자리 색을 보정했습니다. 원본에서 알파를 복원한 추정치이므로 원본 외관을 엄밀히 유지하려면 흰 배경 버전을 쓰세요.
- 확대 PNG는 보간한 것이며 벡터가 아닙니다. 큰 크기에서는 원본 해상도 한계가 있습니다.

## 패키지 연결
Assets 폴더를 프로젝트에 포함하고 패키지 리소스로 빌드하세요. Manifest에는 배율 없는 논리 파일명을 참조합니다(실제 파일은 .scale-100 등 배율 한정자 포함).
- Properties/Logo: Assets\StoreLogo.png
- uap:VisualElements의 Square44x44Logo: Assets\Square44x44Logo.png
- uap:VisualElements의 Square150x150Logo: Assets\Square150x150Logo.png
- uap:DefaultTile의 Square71x71Logo, Wide310x150Logo, Square310x310Logo: 같은 이름의 Assets\*.png
- uap:SplashScreen Image: Assets\SplashScreen.png

300×300은 Square150x150Logo.scale-200.png입니다. 125%의 150→188, 50→63, 310→388은 Microsoft 표에 맞게 반올림했습니다.
Target-size에는 기본·unplated·lightunplated 파일을 제공합니다. 44px은 추가 선택 크기입니다. 밝은/어두운 테마 모두 같은 컬러 로고를 사용합니다.
타일·스플래시는 앱/manifest에 따라 선택 사항입니다. 모든 파일을 반드시 사용해야 하는 것은 아니며 이 묶음은 Store 등록용 스크린샷이나 MSIX 패키지 자체가 아닙니다. 실제 빌드·Store 검증은 별도로 진행하세요.

공식 규격 참고: https://learn.microsoft.com/en-us/windows/apps/design/iconography/app-icon-construction
