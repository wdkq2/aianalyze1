# aianalyze1

This repository includes a Colab notebook for collecting press release PDFs from the Korean Ministry of Land, Infrastructure and Transport (국토교통부). The notebook downloads PDFs, extracts text, creates embeddings and saves results to Google Drive.

Open `bodo_pdf_colab.ipynb` with Google Colab to run the workflow. The notebook
expects a JSON configuration file on your Google Drive containing API keys and
paths. Example `env.json`:

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

Set `CONFIG_PATH` in the first cell of the notebook to the location of this file
and the rest of the variables will load automatically.
