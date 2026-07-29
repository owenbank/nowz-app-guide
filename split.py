#!/usr/bin/env python3
"""
단일 파일 HTML(모든 SVG가 인라인)을 index.html + screens/ 로 분리한다.

사용법:
    python3 split.py ~/Downloads/index.html

피그마에서 만든 설명서를 지금까지처럼 통짜 HTML 한 개로 받아도,
이 스크립트를 돌리면 GitHub에 올릴 수 있는 형태로 바뀐다.
뷰어 코드는 건드리지 않는다 (원래부터 screens/ 폴백을 지원함).
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSET = re.compile(
    r'<script type="text/plain" class="svg-asset" data-file="([^"]+)">(.*?)</script>\s*',
    re.S,
)
REGISTRY = re.compile(r'<script>window\.SVG_REGISTRY=\{\};.*?</script>\s*', re.S)


def main():
    if len(sys.argv) != 2:
        sys.exit(f"사용법: python3 {os.path.basename(__file__)} <단일파일.html>")

    src = os.path.expanduser(sys.argv[1])
    if not os.path.isfile(src):
        sys.exit(f"파일을 찾을 수 없습니다: {src}")

    html = open(src, encoding="utf-8").read()

    screens = {}
    html = ASSET.sub(lambda m: screens.__setitem__(m.group(1), m.group(2)) or "", html)
    if not screens:
        sys.exit("인라인 SVG(script.svg-asset)를 찾지 못했습니다. 이미 분리된 파일인가요?")
    html = REGISTRY.sub("", html)

    out_dir = os.path.join(HERE, "screens")
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir)
    for name, content in screens.items():
        open(os.path.join(out_dir, name), "w", encoding="utf-8").write(content.strip())

    index = os.path.join(HERE, "index.html")
    open(index, "w", encoding="utf-8").write(html)

    # APPS 가 참조하는 파일이 전부 있는지 확인
    refs = set(re.findall(r'file:\s*"([^"]+\.svg)"', html))
    missing = sorted(refs - set(screens))
    unused = sorted(set(screens) - refs)

    mb = os.path.getsize(src) / 1024 / 1024
    kb = os.path.getsize(index) / 1024
    print(f"index.html : {mb:.1f} MB -> {kb:.0f} KB")
    print(f"screens/   : {len(screens)}개")
    if missing:
        print(f"⚠️  APPS가 참조하지만 없는 파일: {missing}")
    if unused:
        print(f"⚠️  어디서도 쓰이지 않는 파일: {unused}")
    if not missing and not unused:
        print("검사 통과 — GitHub Desktop에서 Commit 후 Push 하세요.")


if __name__ == "__main__":
    main()
