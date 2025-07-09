# aianalyze1

이 저장소는 국토교통부 보도자료 PDF를 수집해 텍스트와 임베딩을 생성하는 Google Colab 노트북과 동일한 파이썬 스크립트를 제공합니다.

## 빠른 시작
`bodo_pdf_colab.ipynb` 파일을 Google Colab에서 열어 실행할 수 있습니다. 노트북은 Google Drive에 위치한 JSON 설정 파일을 사용합니다. 예시는 다음과 같습니다.

```json
{
  "SERVICE_KEY": "YOUR_URL_ENCODED_SERVICE_KEY",
  "DCLSF_CD": "A00",
  "START_DATE": "2020-01-01",
  "END_DATE": "2025-07-08",
  "PAGE_SIZE": 1000,
  "DRIVE_DIR": "/content/drive/MyDrive/boan_data",
  "HF_HOME_DIR": "/content/drive/.hf_cache"
}
```

첫 번째 셀의 `CONFIG_PATH` 변수에 이 파일의 경로를 지정하면 나머지 값이 자동으로 불러와집니다.

## 자세한 사용 방법 (처음부터 끝까지)

### 1. 준비 단계
1. [data.go.kr](https://www.data.go.kr)에서 "일반(Decoding) 서비스키"를 발급받습니다.
2. Google Drive에서 `env.json`이라는 새 파일을 만들고 위의 예시 내용을 복사해 넣습니다. `SERVICE_KEY`에는 방금 발급받은 키를 입력하고 필요에 따라 다른 값도 수정한 뒤 저장합니다.

### 2. 노트북 실행
1. [Google Colab](https://colab.research.google.com)에 접속해 상단 메뉴에서 **파일 > GitHub에서 열기**를 클릭합니다.
2. 이 저장소 주소를 입력해 `bodo_pdf_colab.ipynb`를 선택합니다.
3. 첫 번째 코드 셀의 `CONFIG_PATH` 변수에 드라이브에 저장한 `env.json`의 전체 경로(예: `/content/drive/MyDrive/boan_data/env.json`)를 입력합니다.
4. 셀을 위에서 아래로 순서대로 실행합니다. 처음 셀에서는 필요한 패키지를 설치하고 구글 드라이브를 마운트하므로 권한 요청이 나타나면 허용합니다.
5. 이후 셀들은 자동으로 API에서 PDF 목록을 받아 내려받고, 텍스트 추출과 임베딩을 수행합니다.

### 3. 결과 확인
모든 셀 실행이 완료되면 `docs.db`와 `faiss_index.faiss` 파일이 `DRIVE_DIR`에 지정한 폴더에 저장됩니다. 구글 드라이브에서 해당 폴더를 열어 파일이 생성되었는지 확인하세요. 노트북 하단에는 처리한 PDF 개수와 저장 경로가 출력됩니다.

## 커맨드라인 스크립트 사용
Colab이 아닌 환경에서는 `bodo_pdf.py` 스크립트로 동일한 작업을 수행할 수 있습니다.

```bash
python bodo_pdf.py --config /path/to/env.json
```

`env.json` 형식은 위와 동일하며 실행 후 결과 파일이 `DRIVE_DIR`에 저장됩니다.

