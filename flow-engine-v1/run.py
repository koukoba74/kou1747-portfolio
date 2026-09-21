from pathlib import Path
import csv, json, re, html

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "input"
PAGES = ROOT / "output" / "pages"
REPORTS = ROOT / "reports"
PAGES.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

REQUIRED = ["slug","title","summary","body","tags","image_src","image_alt"]

def safe_slug(value):
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9_-]+", "-", value)
    return value.strip("-")

def read_rows():
    with (INPUT / "content.csv").open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def validate_input(rows):
    errors = []
    seen = set()
    for i, row in enumerate(rows, start=2):
        for key in REQUIRED:
            if not (row.get(key) or "").strip():
                errors.append({"row": i, "slug": row.get("slug",""), "type": "missing_required", "detail": key})
        slug = safe_slug(row.get("slug"))
        if not slug:
            errors.append({"row": i, "slug": "", "type": "invalid_slug", "detail": row.get("slug","")})
        elif slug in seen:
            errors.append({"row": i, "slug": slug, "type": "duplicate_slug", "detail": slug})
        seen.add(slug)
    return errors

def render_page(template, row):
    tags = [t.strip() for t in (row["tags"] or "").split("|") if t.strip()]
    tags_html = "".join(f'<span class="tag">{html.escape(t)}</span>' for t in tags)
    repl = {
        "{{TITLE}}": html.escape(row["title"]),
        "{{SUMMARY}}": html.escape(row["summary"]),
        "{{BODY}}": html.escape(row["body"]).replace("\n","<br>"),
        "{{TAGS_HTML}}": tags_html,
        "{{IMAGE_SRC}}": html.escape(row["image_src"], quote=True),
        "{{IMAGE_ALT}}": html.escape(row["image_alt"], quote=True),
    }
    page = template
    for k,v in repl.items():
        page = page.replace(k,v)
    return page

def qa_page(path):
    text = path.read_text(encoding="utf-8")
    issues = []
    if len(re.findall(r"<h1(?:\s|>)", text, re.I)) != 1:
        issues.append("h1_count")
    if not re.search(r"<title>.+?</title>", text, re.I|re.S):
        issues.append("title_missing")
    if re.search(r"\{\{[A-Z0-9_]+\}\}", text):
        issues.append("placeholder_remaining")
    for alt in re.findall(r'<img\b[^>]*\balt="([^"]*)"', text, re.I):
        if not alt.strip():
            issues.append("empty_alt")
    if "../index.html" not in text:
        issues.append("back_link_missing")
    return issues

rows = read_rows()
input_errors = validate_input(rows)
bad_rows = {e["row"] for e in input_errors}
template = (INPUT / "template.html").read_text(encoding="utf-8")

generated = []
for csv_row, row in enumerate(rows, start=2):
    if csv_row in bad_rows:
        continue
    slug = safe_slug(row["slug"])
    path = PAGES / f"{slug}.html"
    path.write_text(render_page(template, row), encoding="utf-8")
    generated.append((slug, row["title"], row["summary"], path))

cards = "\n".join(
    f'<li><a href="pages/{html.escape(slug)}.html"><strong>{html.escape(title)}</strong></a><br>{html.escape(summary)}</li>'
    for slug,title,summary,_ in generated
)
index = f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>生成ページ一覧</title></head><body style="font-family:system-ui,sans-serif;max-width:860px;margin:40px auto;padding:0 20px">
<h1>生成ページ一覧</h1><p>CSVから自動生成したページです。</p><ul>{cards}</ul></body></html>'''
(ROOT / "output" / "index.html").write_text(index, encoding="utf-8")

qa_rows = []
for slug,title,summary,path in generated:
    issues = qa_page(path)
    qa_rows.append({"slug":slug, "status":"FAIL" if issues else "PASS", "issues":"|".join(issues)})

with (REPORTS / "qa_report.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["slug","status","issues"])
    w.writeheader(); w.writerows(qa_rows)

with (REPORTS / "errors.csv").open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["row","slug","type","detail"])
    w.writeheader(); w.writerows(input_errors)

summary = {
    "input_rows": len(rows),
    "generated_pages": len(generated),
    "input_errors": len(input_errors),
    "qa_failures": sum(1 for x in qa_rows if x["status"]=="FAIL"),
    "status": "PASS" if not input_errors and all(x["status"]=="PASS" for x in qa_rows) else "REVIEW_REQUIRED"
}
(REPORTS / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False))
