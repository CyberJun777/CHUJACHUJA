#!/bin/bash
# 공유 폴더(/mnt/project-files/결항앱)의 최신 화면을 저장소 사본에 가져와 APK·HTML을 다시 만들고 올린다.
# 사용: ./sync_build.sh "커밋 제목"
set -euo pipefail
cd "$(dirname "$0")"
S=/mnt/project-files/결항앱; P=/mnt/project-files
git pull -q --no-edit origin "$(git rev-parse --abbrev-ref HEAD)"
cp $S/*.py $S/*.css $S/guide.tpl.html $S/chuja-guide.html $S/tpl.html 결항앱/
rm -f 결항앱/*.before_manus.py; rm -rf 결항앱/photos; cp -r $S/photos 결항앱/
(cd 안드로이드앱/빌드소스 && ./build.sh 2>&1 | tail -2)
cp 안드로이드앱/빌드소스/out/sinyang-sori.apk 안드로이드앱/신양애소리.apk
git add -A
git diff --cached --quiet || git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "${1:-앱 화면 변경 반영}" -m "Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01MzEymZ44i8GdMDDE3hvrkM"
git push -q origin "$(git rev-parse --abbrev-ref HEAD)" 2>&1 | grep -v "moved\|CHUJACHUJA.git" || true
cp 안드로이드앱/신양애소리.apk $P/안드로이드앱/; cp 신양애소리.html $P/깃허브/
git status -sb | head -1
