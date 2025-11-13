# tools/clean_signals.py
"""
Clean and reorganize signal files into structured folders:
- ml/signals/master/  -> consolidated master file(s)
- ml/signals/tickers/ -> latest per-ticker files (keep-last N)
- ml/signals/archive/ -> older files moved to archive
- ml/signals/latest/  -> optional place for very latest
Usage:
    python tools/clean_signals.py --keep-last 3
Notes:
- This script moves files; ensure you have backups if needed.
"""
import argparse
from pathlib import Path
import shutil

ROOT = Path("ml/signals")
MASTER = ROOT / "master"
TICKERS = ROOT / "tickers"
ARCHIVE = ROOT / "archive"
LATEST = ROOT / "latest"

for d in [MASTER, TICKERS, ARCHIVE, LATEST]:
    d.mkdir(parents=True, exist_ok=True)

def is_signal_file(p: Path):
    return p.is_file() and p.suffix.lower() == ".csv" and p.name.startswith("generated_signals")

def main(keep_last:int):
    # collect all signal files in root (not in structured folders)
    files = sorted([p for p in ROOT.iterdir() if is_signal_file(p)], key=lambda x: x.stat().st_mtime, reverse=True)
    # move master files explicitly to master/
    for f in files:
        if "master" in f.name.lower():
            shutil.move(str(f), str(MASTER / f.name))
    # refresh list after moving masters
    files = sorted([p for p in ROOT.iterdir() if is_signal_file(p)], key=lambda x: x.stat().st_mtime, reverse=True)
    # group by ticker using name parsing
    ticker_map = {}
    for f in files:
        parts = f.name.split("_")
        # try to extract ticker as the 3rd or 4th element, tolerantly
        ticker = "UNKNOWN"
        for part in parts:
            # detect uppercase ticker-like tokens
            if part.isupper() and any(c.isalpha() for c in part):
                ticker = part
                break
        ticker_map.setdefault(ticker, []).append(f)
    # move files: keep last N per ticker in tickers/, others to archive/
    for ticker, flist in ticker_map.items():
        flist_sorted = sorted(flist, key=lambda x: x.stat().st_mtime, reverse=True)
        for i, f in enumerate(flist_sorted):
            target = TICKERS if i < keep_last else ARCHIVE
            shutil.move(str(f), str(target / f.name))
    print("[CLEAN] Signals reorganized into master/, tickers/, archive/, latest/")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--keep-last", type=int, default=3, help="how many recent per ticker to keep in tickers/")
    args = parser.parse_args()
    main(args.keep_last)
