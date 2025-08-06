import os
import re
import sys
import json
import hashlib
import datetime
from collections import defaultdict

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

HTML_REPORT = "privacy_report.html"

# --- Privacy-related regex patterns
PII_PATTERNS = {
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "phone": r"\b(\+?\d{1,2}\s?)?(\()?(\d{3})(\))?[\s.-]?(\d{3})[\s.-]?(\d{4})\b",
    "ssn": r"\b\d{3}[- ]?\d{2}[- ]?\d{4}\b",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b"
}

# --- Utility: hash file for duplicate detection
def hash_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

# --- Metadata Extraction
def get_metadata(path):
    try:
        stat = os.stat(path)
        created = datetime.datetime.fromtimestamp(stat.st_ctime)
        modified = datetime.datetime.fromtimestamp(stat.st_mtime)
        size = stat.st_size
    except Exception:
        created = modified = size = None
    extras = {}
    if path.lower().endswith(".pdf") and PdfReader:
        try:
            reader = PdfReader(path)
            meta = reader.metadata or {}
            extras['pdf_title'] = getattr(meta, "title", "")
            extras['pdf_author'] = getattr(meta, "author", "")
        except Exception:
            pass
    return {"created": created, "modified": modified, "size": size, **extras}

# --- Filesystem/Report Scanner
def scan_folder(folder):
    pii_matches = defaultdict(list)
    all_files = []
    hashes = {}
    duplicates = defaultdict(list)
    metadata_issues = []
    risky_files = []
    for root, _, files in os.walk(folder):
        for fname in files:
            fpath = os.path.join(root, fname)
            all_files.append(fpath)
            info = get_metadata(fpath)
            # Check for old files, geo/author data in PDF, etc.
            if ('pdf_author' in info and info['pdf_author']) or ('pdf_title' in info and info['pdf_title']):
                metadata_issues.append((fpath, info))
            if info['created'] and (datetime.datetime.now() - info['created']).days > 2*365:
                metadata_issues.append((fpath, info))
            # Content scan for PII (on small txt/pdf only)
            if os.path.getsize(fpath) < 2*1024*1024:  # 2 MB
                try:
                    text = ""
                    if fpath.lower().endswith(".txt"):
                        with open(fpath, "r", encoding="utf8", errors="ignore") as f:
                            text = f.read()
                    elif fpath.lower().endswith(".pdf") and PdfReader:
                        reader = PdfReader(fpath)
                        for page in reader.pages[:4]:
                            text += page.extract_text() or ""
                    for kind, pattern in PII_PATTERNS.items():
                        for match in re.findall(pattern, text):
                            pii_matches[kind].append((fpath, match))
                except Exception:
                    pass
            # Hash for duplicates
            h = hash_file(fpath)
            if h:
                if h in hashes:
                    duplicates[h].append(fpath)
                else:
                    hashes[h] = fpath
            # Very permissive risky extension check
            if fname.lower().endswith(('.bak', '.tmp', '.old', '.backup')):
                risky_files.append(fpath)
    return {
        "all_files": all_files,
        "pii_matches": pii_matches,
        "metadata_issues": metadata_issues,
        "duplicates": duplicates,
        "risky_files": risky_files
    }

# --- Privacy Risk Scoring
def compute_score(report):
    score = 0
    score -= 30 * sum(len(v) for v in report['pii_matches'].values())
    score -= 10 * len(report['metadata_issues'])
    score -= 15 * len(report['risky_files'])
    score -= 20 * sum(len(v) for v in report['duplicates'].values())
    return max(0, 100 + score)

# --- Generate HTML Report
def html_report(folder, report, score):
    h = ["<html><head><title>Privacy Risk Report</title></head><body>"]
    h.append(f"<h1>Privacy Analyzer Report for {folder}</h1>")
    h.append(f"<h2>Privacy Risk Score: <span style='color: {'red' if score<70 else 'orange' if score<90 else 'green'}'>{score}/100</span></h2>")
    h.append("<h3>Summary:</h3><ul>")
    h.append(f"<li>Files scanned: {len(report['all_files'])}</li>")
    h.append(f"<li>PII Findings: {sum(len(v) for v in report['pii_matches'].values())}</li>")
    h.append(f"<li>Metadata issues: {len(report['metadata_issues'])}</li>")
    h.append(f"<li>Duplicate files: {sum(len(v) for v in report['duplicates'].values())}</li>")
    h.append(f"<li>Risky files: {len(report['risky_files'])}</li>")
    h.append("</ul>")
    if report['pii_matches']:
        h.append(f"<h3>Potential PII Leaks</h3><ul>")
        for kind, matches in report['pii_matches'].items():
            for f, match in matches:
                h.append(f"<li>{kind}: <code>{match}</code> in <i>{f}</i></li>")
        h.append("</ul>")
    if report['metadata_issues']:
        h.append("<h3>Files with risk-significant metadata (old, author info):</h3><ul>")
        for fpath, minfo in report['metadata_issues']:
            h.append(f"<li>{fpath} ({minfo})</li>")
        h.append("</ul>")
    if report['duplicates']:
        h.append(f"<h3>Duplicates</h3><ul>")
        for k, dups in report['duplicates'].items():
            h.append(f"<li>Duplicate group ({len(dups)+1} files): <ul>")
            h.append(f"<li>{k}</li>")
            for fname in dups:
                h.append(f"<li>{fname}</li>")
            h.append("</ul></li>")
        h.append("</ul>")
    if report['risky_files']:
        h.append("<h3>Files with risky extensions (.bak/.old/.tmp):</h3><ul>")
        for fname in report['risky_files']:
            h.append(f"<li>{fname}</li>")
        h.append("</ul>")
    h.append("<h3>Recommendations:</h3>")
    h.append("<ul>")
    h.append("<li>Remove or sanitize files with plaintext PII.</li>")
    h.append("<li>Delete unnecessary duplicate/backups or risky file extensions.</li>")
    h.append("<li>Strip author/creation metadata from shared documents, especially PDFs.</li>")
    h.append("</ul>")
    h.append("</body></html>")
    with open(HTML_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(h))
    print(f"\nHTML report written to: {HTML_REPORT}")

# --- Main ---
def main():
    folder = input("Enter folder to scan for privacy risk (or leave blank for current dir): ").strip()
    if not folder:
        folder = os.getcwd()
    print(f"\nScanning {folder} ...")
    report = scan_folder(folder)
    score = compute_score(report)
    print(f"\nPrivacy risk score: {score}/100")
    # Output simple CLI summary
    for k,v in report['pii_matches'].items():
        if v: print(f"Found potential {k} in files: {[f for f,_ in v]}")
    if report['metadata_issues']:
        print(f"Files with privacy-leaking metadata: {[f for f,_ in report['metadata_issues']]}")
    if report['duplicates']:
        print(f"Duplicate files detected: {sum(len(v) for v in report['duplicates'].values())}")
    if report['risky_files']:
        print(f"Files with risky extensions: {report['risky_files']}")
    html_report(folder, report, score)

if __name__ == "__main__":
    if PdfReader is None:
        print("Install PyPDF2 for PDF support: pip install PyPDF2")
    main()
