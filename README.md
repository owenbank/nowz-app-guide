# 나우즈 사용설명서 — 수정 안내

사이트: https://nowz-app-guide.vercel.app

**main에 커밋하면 Vercel이 자동 배포합니다.** 별도 배포 작업 없음. 반영까지 약 1분.

## 파일 구조

| 경로 | 내용 |
|---|---|
| `index.html` | 뷰어 + 목차 데이터 (117KB) |
| `screens/*.svg` | 화면 이미지 52개 |
| `split.py` | 통짜 HTML → 분리 변환기 |
| `check.py` | 화면 파일 규격 검사기 |

---

## 0. 피그마에서 내보내는 규격 ⭐

**가장 중요합니다. 여기만 맞으면 나머지는 파일 올리는 일뿐입니다.**

| 항목 | 값 |
|---|---|
| 폭 | **375** (1x 로 내보내기) |
| 포맷 | **SVG** |
| 범위 | **본문 제목부터** — 상태바·헤더·브레드크럼 제외 |

마지막 항목이 핵심입니다. 피그마 프레임에는 상태바(9:41)와 `☰ 학생앱 사용설명서` 헤더, 브레드크럼이 들어있지만 **사이트가 그 부분을 이미 HTML로 그립니다.** 같이 내보내면 헤더가 두 번 보입니다.

내보낸 뒤 확인:

```
python3 check.py 새화면.svg
```

---

## 1. 화면 하나 고치기 (가장 흔함)

**index.html은 건드리지 않습니다. 파일명만 같으면 됩니다.**

1. GitHub에서 `screens` 폴더 열기
2. **Add file → Upload files**
3. 피그마에서 내보낸 SVG를 **기존과 똑같은 파일명으로** 드래그
4. **Commit changes**

## 2. 화면 추가하기

먼저 위 1~4번으로 새 SVG를 `screens/`에 올린 뒤,

1. `index.html` → 연필 아이콘(Edit this file)
2. `const APPS` 안에서 새 화면이 들어갈 **바로 앞 화면 줄을 찾아** 그 아래에 추가
3. **Commit changes**

```js
{ file: "home-alarm.svg",  major: "홈",  minor: "알림" },
```

- `major` = 사이드바 대분류 / `minor` = 소분류 (단독 항목이면 `null`)
- **배열 순서 = 페이지 순서**
- 학생앱은 `student:` 블록, 학부모앱은 `parent:` 블록

## 3. 순서 바꾸기

`index.html`의 `pages` 배열에서 해당 줄의 위치만 위아래로 옮기면 됩니다.

## 3-1. 올리기 전 확인 (선택)

```
cd ~/Downloads/nowz-app-guide && python3 check.py
```

참조는 있는데 파일이 없는 경우(=화면이 안 뜸), 파일은 있는데 목차에 없는 경우, 규격이 어긋난 경우를 잡아줍니다.

## 4. 통짜 HTML을 새로 만들었을 때

피그마에서 설명서 전체를 HTML 한 개로 뽑았다면:

```
cd ~/Downloads/nowz-app-guide
python3 split.py ~/Downloads/index.html
```

분리 + 누락 파일 검사까지 자동. 그다음 GitHub Desktop에서 Commit → Push.

---

## 선택 항목

| 위치 | 용도 | 안 하면 |
|---|---|---|
| `SEARCH_TEXT` | 화면 본문 검색 색인 | 본문 검색만 안 됨 (분류명 검색은 정상) |
| `SCREEN_LINKS` | 화면 위 파란 링크 클릭 영역 (% 좌표) | 해당 화면에 클릭 링크가 없을 뿐 |

둘 다 손으로 쓰기 번거로우니 필요할 때 채우면 됩니다.

---

## 주의

- **한 파일에 다 넣지 마세요.** 예전엔 19.5MB 단일 HTML이었는데, GitHub 브라우저 업로드 한도(25MiB)에 걸려 커밋이 실패했습니다.
- 큰 파일 push가 `The remote disconnected`로 끊기면 이미 적용된 로컬 설정(`http.postBuffer`, `http.version`)이 처리합니다. 새로 클론했다면 다시 넣으세요.
- GitHub Desktop 토큰이 만료되면 push가 `Authentication failed`로 실패합니다. **Settings → Accounts**에서 재로그인.
