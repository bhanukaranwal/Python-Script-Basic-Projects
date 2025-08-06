import os
import hashlib
import datetime

BACKUP_LOC = "backup"  # Folder to check for backups
HTML_REPORT = "backup_report.html"

def hash_file(path):
    BUF_SIZE = 65536
    sha = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while True:
                d = f.read(BUF_SIZE)
                if not d:
                    break
                sha.update(d)
    except Exception:
        return None
    return sha.hexdigest()

def scan_folder(folder):
    # Map from hash -> [file paths]
    hashes = {}
    file_times = {}
    all_files = []
    for root, _, files in os.walk(folder):
        for fname in files:
            path = os.path.join(root, fname)
            if not os.path.isfile(path):
                continue
            all_files.append(path)
            h = hash_file(path)
            if h is not None:
                hashes.setdefault(h, []).append(path)
            t = None
            try:
                t = datetime.datetime.fromtimestamp(os.stat(path).st_mtime)
            except Exception:
                pass
            file_times[path] = t
    return all_files, hashes, file_times

def compare_backup(src_files, backup_dir):
    # Given a list of filepaths and backup dir, return missing files (by hash)
    backup_files, backup_hashes, _ = scan_folder(backup_dir)
    backup_hashes_set = set(backup_hashes.keys())
    src_hashes = [hash_file(f) for f in src_files]
    missing = []
    for f, h in zip(src_files, src_hashes):
        if h and h not in backup_hashes_set:
            missing.append(f)
    return missing

def html_report(dup_map, missing, risky, backup_loc):
    h = ["<html><head><title>Backup, Deduplication, Recovery Report</title></head><body>"]
    h.append(f"<h1>Personal Backup & Recovery Advisor</h1>")
    h.append(f"<h2>Backup location checked: {backup_loc}</h2>")
    h.append(f"<p>Total duplicate sets: {len(dup_map)}</p>")
    if dup_map:
        h.append("<h3>Duplicate Files</h3><ul>")
        for k, v in dup_map.items():
            if len(v) > 1:
                h.append(f"<li>{len(v)} duplicates: <ul>")
                for f in v:
                    h.append(f"<li>{f}</li>")
                h.append("</ul></li>")
        h.append("</ul>")
    if missing:
        h.append(f"<h3>Files Missing in Backup</h3><ul>")
        for f in missing:
            h.append(f"<li>{f}</li>")
        h.append("</ul>")
    if risky:
        h.append(f"<h3>Risky Files (by extension)</h3><ul>")
        for f in risky:
            h.append(f"<li>{f}</li>")
        h.append("</ul>")
    h.append("<h3>Recommendations:</h3><ul>")
    h.append("<li>Delete duplicate files to save space.</li>")
    h.append(f"<li>Backup {len(missing)} missing files as priority.</li>")
    h.append("<li>Consider compressing old files, check risky temp files for sensitive data.</li>")
    h.append("</ul></body></html>")
    with open(HTML_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(h))
    print(f"\nHTML report written to: {HTML_REPORT}")

def main():
    folder = input("Enter folder to scan (blank=current): ").strip() or "."
    backup_dir = input(f"Backup folder (blank={BACKUP_LOC}): ").strip() or BACKUP_LOC
    print(f"\nScanning main folder: {folder}\nScanning backup: {backup_dir} ...")
    all_files, hashes, file_times = scan_folder(folder)
    # Find duplicates (hashes with >1 file)
    dup_map = {k:v for k,v in hashes.items() if len(v) > 1}
    # Files missing in backup
    missing = compare_backup(all_files, backup_dir)
    # Risky extensions
    risky = [f for f in all_files if f.lower().endswith(('.bak', '.tmp', '.old', '.backup'))]
    print("\nSummary:")
    print(f"Duplicate sets: {len(dup_map)}")
    print(f"Files missing in backup: {len(missing)}")
    print(f"Risky files (by extension): {len(risky)}")
    html_report(dup_map, missing, risky, backup_dir)

if __name__ == "__main__":
    main()
