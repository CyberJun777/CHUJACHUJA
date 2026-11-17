# 신양愛소리 안드로이드 APK 빌드

`결항앱/chuja-guide.html`(앱 화면)을 글꼴과 함께 APK 안에 담아 WebView로 보여 주는 껍데기 앱이다. 화면 원본의 스크립트·자료·확률 계산식은 고치지 않는다.

## 자료가 갱신되는 방식
- 저장소의 `data/live.json`이 오전 6시~오후 8시(한국 시간)에 한 시간마다 그 시각의 운항 편성·부이 관측·해상예보로 바뀐다(저장소 루트의 `update.sh`).
- 앱은 열릴 때(그리고 다시 화면에 나올 때) 이 파일을 받아, 내장 자료보다 새것이면 기기에 저장하고 화면을 한 번 다시 연다. 그러면 원본 스크립트가 새 자료로 확률을 다시 계산한다. (`live-update.js`, `prep.py`가 화면에 덧붙임)
- 받지 못하면 마지막으로 받은 자료(없으면 내장 자료)를 쓰고, 그 자료가 오늘 것이 아니면 "몇 월 며칠 자료"라는 안내 띠를 보여 준다.
- 과거 운항 기록(확률 계산의 바탕)은 APK에 내장되어 있고 매일 바뀌지 않는다.

## 다시 만들기
`./build.sh` → `out/sinyang-sori.apk`. 앱 이름은 `app/res/values/strings.xml`의 `app_name`.

필요한 도구(안드로이드 SDK 없이 구성, `tools/`에 직접 받아 둔다):
- aapt2: `pip install aapt2`
- `tools/android-all.jar`: Maven Central `org.robolectric:android-all:14-robolectric-10818077`
- `tools/dx.jar`: Maven Central `com.jakewharton.android.repackaged:dalvik-dx:9.0.0_r3`
- `tools/apksig.jar`: Maven Central `com.android.tools.build:apksig:2.3.0` (v2 서명만 사용, `tools/signer/Sign.java`)
- JDK 17 이상, zip, python3

## 서명 키
시연용 서명 키 `tools/demo.keystore`는 공개 저장소에 올리지 않았다(PC 폴더에만 있음). 키가 없으면 `build.sh`가 새 키를 만드는데, 그 APK는 기존 설치본 위에 덮어 설치되지 않으므로 먼저 앱을 삭제해야 한다.

## 확인하지 못한 것
에뮬레이터·실기기가 없는 환경에서 만들었다. 서명 검증, APK 구조, 담긴 화면의 동작(자료 수신·저장·오프라인)까지만 데스크톱 크롬으로 확인했다.
