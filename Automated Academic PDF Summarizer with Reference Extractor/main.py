import os
import re
import glob
import pandas as pd

try:
    import pdfplumber
except ImportError:
    pdfplumber = None
try:
    from transformers import pipeline
    SUMMARIZER = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except:
    SUMMARIZER = None

SUMMARY_LEN = 130

def extract_text(path):
    if not pdfplumber:
        return ""
    try:
        with pdfplumber.open(path) as pdf:
            text = ""
            for i, page in enumerate(pdf.pages[:8]):
                text += page.extract_text() + "\n"
            return text
    except Exception:
        return ""

def extract_title(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines[0] if lines else ""

def extract_abstract(text):
    abs_match = re.search(r'(?i)(abstract[\.:]?)(.*?)\n\n', text, re.DOTALL)
    if abs_match:
        return abs_match.group(2)[:800].replace('\n', ' ')
    # Fallback: First ~1000 characters after title
    return text.split('\n', 2)[-1][:800]

def extract_references(text):
    refs = []
    ref_start = text.lower().find("references")
    if ref_start == -1: ref_start = text.lower().find("bibliography")
    if ref_start > 0:
        ref_block = text[ref_start:]
        refs = re.findall(r'\[\d+\](.*?)(?=\n\[|$)', ref_block, re.DOTALL)  # [12] Ref
        if not refs:
            refs = re.findall(r'\d+\.\s(.*?)(?=\n\d+\.|$)', ref_block, re.DOTALL)  # 1. Ref
    return [r.strip().replace('\n'," ") for r in refs if r.strip()]

def summarize(text):
    if SUMMARIZER and text:
        try:
            return SUMMARIZER(text, max_length=SUMMARY_LEN, min_length=40, do_sample=False)[0]['summary_text']
        except Exception:
            return text[:SUMMARY_LEN*2]
    return text[:SUMMARY_LEN*2]

def process_pdf(path):
    raw = extract_text(path)
    title = extract_title(raw)
    abstract = extract_abstract(raw)
    summary = summarize(abstract)
    refs = extract_references(raw)
    return {"file": os.path.basename(path), "title": title, "summary": summary, "num_refs": len(refs), "refs": refs[:7]}

def cluster_references(all_refs):
    # Basic frequency count by cleaned first 60 chars
    flat = [r[:60].strip().lower() for refs in all_refs for r in refs]
    ser = pd.Series(flat)
    common = ser.value_counts().head(10)
    return common

def main():
    folder = input("PDFs folder (blank=current): ").strip() or '.'
    pdfs = glob.glob(os.path.join(folder, "*.pdf"))
    print(f"Found {len(pdfs)} PDFs.")
    rows = []
    for path in pdfs:
        print(f"Processing: {os.path.basename(path)}")
        doc = process_pdf(path)
        rows.append(doc)
    df = pd.DataFrame(rows)
    out = "pdf_summary.csv"
    df_out = df[["file","title","summary","num_refs"]]
    df_out.to_csv(out, index=False)
    print(f"\nSummary table written to {out}")
    # Show most-cited refs
    all_refs = df["refs"].tolist()
    commonrefs = cluster_references(all_refs)
    print("\nMost Frequently Cited References (by similarity):")
    for i, (k, v) in enumerate(commonrefs.items()):
        print(f"{i+1}. {k}...  ({v} times)")
    # Optionally, HTML
    df_out.to_html("pdf_summary.html", index=False)
    print("Also saved as pdf_summary.html")

if __name__ == "__main__":
    if not pdfplumber:
        print("Please install pdfplumber: pip install pdfplumber")
    main()
