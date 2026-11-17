#!/bin/bash
# 신양愛소리 APK 빌드. 사용: ./build.sh  (결과: out/sinyang-sori.apk)
set -euo pipefail
export LC_ALL=C.UTF-8   # 폴더 이름에 한글이 있어도 자바가 경로를 읽도록
cd "$(dirname "$0")"
AAPT2=$(python3 -c "import aapt2,os;print(os.path.join(os.path.dirname(aapt2.__file__),'bin','Linux','aapt2'))")
JAR=tools/android-all.jar
chmod +x "$AAPT2" 2>/dev/null || true
rm -rf out && mkdir -p out/cls out/dex
python3 prep.py
$AAPT2 compile --dir app/res -o out/res.zip
$AAPT2 link -o out/base.apk -I $JAR --manifest app/AndroidManifest.xml -A app/assets \
  --min-sdk-version 24 --target-sdk-version 34 --version-code 2 --version-name 1.1 out/res.zip
javac -nowarn --release 8 -cp $JAR -d out/cls $(find app/src -name '*.java') 2>&1 | grep -v "warning\|JAVA_TOOL" || true
java -cp tools/dx.jar com.android.dx.command.Main --dex --min-sdk-version=24 --output=out/dex/classes.dex out/cls 2>&1 | grep -v JAVA_TOOL || true
(cd out/dex && zip -q ../base.apk classes.dex)
python3 align.py out/base.apk out/aligned.apk
javac -nowarn -cp tools/apksig.jar -d tools/signer tools/signer/Sign.java 2>&1 | grep -v JAVA_TOOL || true
[ -f tools/demo.keystore ] || keytool -genkeypair -keystore tools/demo.keystore -storepass android -keypass android \
  -alias demo -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Sinyang Sori Demo" 2>/dev/null
java --add-exports java.base/sun.security.x509=ALL-UNNAMED --add-exports java.base/sun.security.pkcs=ALL-UNNAMED --add-opens java.base/sun.security.x509=ALL-UNNAMED -cp tools/apksig.jar:tools/signer Sign tools/demo.keystore out/aligned.apk out/sinyang-sori.apk 2>&1 | grep -v JAVA_TOOL
ls -la out/sinyang-sori.apk
