#!/usr/bin/env python3
"""
screens/ 안의 SVG가 규격에 맞는지 검사한다.

사용법:
    python3 check.py                 # 전체 검사
    python3 check.py 새화면.svg       # 파일 하나만 검사

검사 항목
  1) index.html 이 참조하는 파일이 실제로 있는지 (없으면 화면이 안 뜸)
  2) 어디서도 안 쓰이는 파일이 있는지
  3) 폭이 375 인지
  4) 상단 헤더가 안 잘린 채로 들어왔는지 (viewBox 가 0 에서 시작하면 의심)
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCREENS = os.path.join(HERE, "screens")


def svg_attrs(path):
    head = open(path, encoding="utf-8").read(600)
    m = re.search(r"<svg([^>]*)>", head)
    if not m:
        return None
    a = m.group(1)
    return {k: (re.search(rf'{k}="([^"]*)"', a) or [None, None])[1]
            for k in ("width", "height", "viewBox", "preserveAspectRatio")}


def check_one(path):
    name = os.path.basename(path)
    at = svg_attrs(path)
    if at is None:
        return [f"{name}: <svg> 태그를 찾을 수 없음 (SVG 파일이 맞나요?)"]

    warns = []
    if at["width"] != "375":
        warns.append(f"{name}: 폭이 {at['width']} 입니다. 피그마에서 375 폭 프레임을 1x 로 내보내세요.")

    vb = (at["viewBox"] or "").split()
    if len(vb) == 4:
        y = float(vb[1])
        if y == 0:
            warns.append(
                f"{name}: viewBox 가 y=0 에서 시작합니다. 상태바·헤더·브레드크럼이 "
                f"같이 들어갔다면 사이트에서 헤더가 두 번 보입니다. "
                f"피그마에서 '본문 제목부터' 선택해 내보내세요."
            )
    else:
        warns.append(f"{name}: viewBox 가 없습니다.")
    return warns


def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
        p = target if os.path.isabs(target) else os.path.join(SCREENS, target)
        if not os.path.isfile(p):
            sys.exit(f"파일 없음: {p}")
        warns = check_one(p)
        print("\n".join("⚠️  " + w for w in warns) if warns else "✅ 규격 통과")
        return

    html = open(os.path.join(HERE, "index.html"), encoding="utf-8").read()
    refs = set(re.findall(r'file:\s*"([^"]+\.svg)"', html))
    have = {os.path.basename(p) for p in glob.glob(os.path.join(SCREENS, "*.svg"))}

    problems = []
    for f in sorted(refs - have):
        problems.append(f"❌ {f}: index.html 이 참조하는데 screens/ 에 없습니다 (화면이 안 뜹니다)")
    for f in sorted(have - refs):
        problems.append(f"⚠️  {f}: screens/ 에 있는데 index.html 이 참조하지 않습니다 (목차에 안 보임)")

    warns = []
    for p in sorted(glob.glob(os.path.join(SCREENS, "*.svg"))):
        warns += check_one(p)

    print(f"화면 {len(have)}개 / index.html 참조 {len(refs)}개\n")
    for line in problems:
        print(line)
    for w in warns:
        print("⚠️  " + w)
    if not problems and not warns:
        print("✅ 전부 통과 — 커밋해도 됩니다.")


if __name__ == "__main__":
    main()
