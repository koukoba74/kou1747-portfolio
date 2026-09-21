# flow-engine-v1

CSV原稿 + HTMLテンプレート + 画像情報から大量ページを生成し、QAレポートとエラー一覧を出す自動化エンジンです。

## 入力
- input/content.csv
- input/template.html

## 出力
- output/pages/*.html
- output/index.html
- reports/qa_report.csv
- reports/errors.csv
- reports/summary.json

## 実行
```bash
python run.py
```
