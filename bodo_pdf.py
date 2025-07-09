import os
import json
import requests
import sqlite3
import faiss
import torch
import pdfplumber
import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


def load_config(path):
    with open(path) as f:
        return json.load(f)


def get_pdf_items(service_key, dclsf_cd, start_date, end_date, page_size):
    items = []
    page = 1
    url = "https://apis.data.go.kr/1613000/genFldPriorInfoDsc/getGenFldList"
    while True:
        params = {
            "serviceKey": service_key,
            "pageNo": page,
            "numOfRows": page_size,
            "dclsfCd": dclsf_cd,
            "startDate": start_date,
            "endDate": end_date,
            "viewType": "json",
        }
        r = requests.get(url, params=params)
        r.raise_for_status()
        body = r.json().get("response", {}).get("body", {})
        cur = body.get("items", [])
        if not cur:
            break
        items.extend(cur)
        if len(cur) < page_size:
            break
        page += 1
    return items


def pdf_to_paragraphs(pdf_url):
    local_path = "/tmp/temp.pdf"
    with open(local_path, "wb") as f:
        f.write(requests.get(pdf_url).content)
    paragraphs = []
    with pdfplumber.open(local_path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            for para in text.split("\n"):
                para = para.strip()
                if 150 <= len(para) <= 500:
                    bbox = (0.0, 0.0, float(page.width), float(page.height))
                    paragraphs.append({"page": page_no, "text": para, "bbox": bbox})
    os.remove(local_path)
    return paragraphs


def main(config_path):
    cfg = load_config(config_path)
    service_key = cfg["SERVICE_KEY"]
    dclsf_cd = cfg.get("DCLSF_CD", "A00")
    start_date = cfg.get("START_DATE", "2020-01-01")
    end_date = cfg.get("END_DATE", "2025-07-08")
    page_size = int(cfg.get("PAGE_SIZE", 1000))
    drive_dir = cfg.get("DRIVE_DIR", "/content/drive/MyDrive/boan_data")
    hf_home = cfg.get("HF_HOME_DIR", "/content/drive/.hf_cache")
    os.makedirs(drive_dir, exist_ok=True)
    os.environ["HF_HOME"] = hf_home

    model_name = "upskyy/e5-large-korean" if torch.cuda.is_available() else "snunlp/KR-SBERT-V40K-klueNLI-augSTS"

    model = SentenceTransformer(model_name)

    conn = sqlite3.connect("docs.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS docs (id INTEGER PRIMARY KEY, pdf_url TEXT, page INT, text TEXT, b0 REAL, b1 REAL, b2 REAL, b3 REAL)"
    )
    index = faiss.IndexFlatIP(1024)

    items = get_pdf_items(service_key, dclsf_cd, start_date, end_date, page_size)
    total_paragraphs = 0

    for item in tqdm(items, desc="PDFs"):
        paras = pdf_to_paragraphs(item["downloadUrl"])
        texts = [p["text"] for p in paras]
        if not texts:
            continue
        vecs = model.encode(texts, batch_size=32, convert_to_numpy=True)
        faiss.normalize_L2(vecs)
        index.add(vecs)
        for vec, p in zip(vecs, paras):
            cur.execute(
                "INSERT INTO docs (pdf_url, page, text, b0, b1, b2, b3) VALUES (?,?,?,?,?,?,?)",
                (item["downloadUrl"], p["page"], p["text"], *p["bbox"]),
            )
        conn.commit()
        total_paragraphs += len(paras)

    faiss.write_index(index, "faiss_index.faiss")
    for fname in ["docs.db", "faiss_index.faiss"]:
        dest = os.path.join(drive_dir, fname)
        with open(fname, "rb") as src, open(dest, "wb") as dst:
            dst.write(src.read())
    print(f"Processed {len(items)} PDFs, {total_paragraphs} paragraphs")
    print("Saved docs.db and faiss_index.faiss to", drive_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process MOLIT press releases")
    parser.add_argument("--config", required=True, help="Path to env.json")
    args = parser.parse_args()
    main(args.config)
