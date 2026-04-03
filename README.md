# 📑 한글 문서(HWP/HWPX) 이미지 자동 추출기 v1.0

한글 문서(`.hwp`, `.hwpx`) 내부에 포함된 이미지 파일들을 자동으로 추출하여 깔끔하게 정리해주는 스마트한 GUI 도구입니다.

## ✨ 주요 기능

- **GUI 인터페이스**: 마우스 클릭만으로 파일이나 폴더를 간편하게 선택할 수 있습니다.
- **스마트 폴더 관리**:
  - 파일 1개 추출 시: `파일명_이미지` 폴더에 즉시 저장 (이중 폴더 방지)
  - 다중 파일/폴더 추출 시: 상위 폴더 내에 문서별로 자동 분류
- **저장 위치 옵션**: 결과물을 '원본 파일 위치' 또는 '실행기(.exe) 위치' 중 선택하여 저장 가능합니다.
- **광범위한 호환성**: 구형(`.hwp`, OLE 방식)과 신형(`.hwpx`, XML/ZIP 방식)을 모두 완벽 지원합니다.
- **초기화 기능**: 버튼 하나로 선택 목록과 로그를 즉시 비우고 새 작업을 시작할 수 있습니다.

## 📂 프로젝트 구조

```text
.
├── core/
│   ├── hwp_parser.py    # HWP(OLE) 분석 및 이미지 추출 핵심 로직
│   └── hwpx_parser.py   # HWPX(XML/ZIP) 분석 및 이미지 추출 핵심 로직
├── gui.py               # 메인 GUI 프로그램 (CustomTkinter 기반)
├── main.py              # 터미널 기반 실행 진입점 (CLI용)
├── memo.txt             # 빌드 가이드 및 개발 노트
├── pyproject.toml       # 프로젝트 설정 및 의존성 관리 (uv 기반)
└── uv.lock              # 의존성 버전 고정 파일
```

## 🚀 시작하기 & 빌드 방법

본 프로젝트는 `uv` 패키지 매니저를 사용합니다. 아래 명령어를 복사하여 터미널에 입력하세요.

### 1. 개발 환경 설정 및 실행

```powershell
# 의존성 설치 (최초 1회)
uv sync

# GUI 프로그램 실행
uv run python gui.py
```

### 2. 단일 실행 파일(.exe) 제작

```powershell
# PyInstaller를 이용한 빌드
uv run pyinstaller --onefile --noconsole --collect-all customtkinter --name "한글이미지추출기" gui.py
```
