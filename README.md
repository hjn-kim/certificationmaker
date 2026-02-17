# certificationmaker

자격증 시험 대비서 자동 생성기 - Gemini AI 기반

## 기능

사용자가 자격증 이름을 입력하면 다음 내용이 포함된 PDF 대비서를 생성합니다:

- **표지** - 자격증명, 생성일 포함
- **목차** - 챕터별 구성
- **이론** - 챕터별 핵심 이론 및 설명
- **기출문제** - 20문항 (객관식 4지선다)
- **정답 및 해설** - 상세 해설 포함

## 설치

```bash
pip install -r requirements.txt
```

한글 폰트 설치 (Ubuntu/Debian):
```bash
sudo apt-get install fonts-nanum
```

## 설정

`.env` 파일을 생성하고 Gemini API 키를 입력합니다:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

API 키는 [Google AI Studio](https://aistudio.google.com/apikey)에서 발급받을 수 있습니다.

## 사용법

```bash
python main.py
```

실행 후 응시할 자격증 이름을 입력하면 `output/` 디렉토리에 PDF가 생성됩니다.

## 프로젝트 구조

```
certificationmaker/
├── main.py                 # CLI 진입점
├── requirements.txt        # 의존성
├── .env                    # Gemini API 키 (직접 생성)
├── src/
│   ├── gemini_client.py    # Gemini API 클라이언트
│   ├── generator.py        # 콘텐츠 생성 로직
│   └── pdf_builder.py      # PDF 생성 모듈
└── output/                 # 생성된 PDF 저장
```
