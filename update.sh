#!/bin/bash
# 그 시각의 운항 편성·부이·예보를 받아 data/live.json 만 갱신해 올린다. (인증키는 환경 변수 KMA_API_KEY, ShipmentKEY)
# 사용: ./update.sh   → 마지막 줄이 "OK ..." 이면 성공
set -uo pipefail
cd "$(dirname "$0")"
BR=$(git rev-parse --abbrev-ref HEAD)
git pull -q --no-edit origin "$BR" || { echo "FAIL pull"; exit 1; }
(cd 결항앱 && timeout 600 python3 refresh.py 2>&1 | grep -v -i "key" | tail -6) || { echo "FAIL refresh"; exit 1; }
python3 publish_live.py || { echo "FAIL publish"; git checkout -q -- 결항앱; exit 1; }
git checkout -q -- 결항앱          # 화면·data.json 은 건드리지 않는다(올리는 것은 live.json 뿐)
if git diff --quiet -- data/live.json; then echo "OK 변동 없음"; exit 0; fi
F=$(python3 -c "import json;print(json.load(open('data/live.json',encoding='utf-8'))['fetched'])")
git add data/live.json
git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "자료 갱신 $F" -m "Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01MzEymZ44i8GdMDDE3hvrkM"
for i in 1 2 3 4; do git push -q origin "$BR" && { echo "OK 올림 $F"; exit 0; }; sleep $((i*4)); done
echo "FAIL push"; exit 1
