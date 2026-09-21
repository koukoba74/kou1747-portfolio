from pathlib import Path
import csv

root = Path(__file__).resolve().parent
out = root / "input" / "content.csv"
with out.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["slug","title","summary","body","tags","image_src","image_alt"])
    for i in range(1, 101):
        w.writerow([
            f"case-{i:03d}",
            f"テストページ{i:03d}",
            f"100ページ生成テスト {i:03d}",
            f"大量流し込みを想定した自動生成テスト本文 {i:03d} です。",
            "HTML|QA|自動化",
            f"https://placehold.co/1200x630?text=Case+{i:03d}",
            f"テストページ{i:03d}の画像"
        ])
print(out)
