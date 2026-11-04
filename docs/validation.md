# 模板驗證紀錄

驗證日期：2026-11-04。驗證範圍為此模板的 synthetic examples 與工具，不是任何公司的產品測試。

## 已完成的本機檢查

| 項目 | 結果 |
| --- | --- |
| pytest（Python 3.14，含 Chrome UI 與 WebSocket） | 30 passed、1 skipped；skip 是未啟用的外部 live lane |
| 10 個 Skills 的官方 quick validator | 全部通過 |
| TOML／JSON／YAML／Python syntax、Markdown links | 通過 |
| Ruff | 通過 |
| Readable Excel | 10 cases、10 step rows；0 errors、0 warnings |
| Report Draft → Word | 結構驗證通過；七章與 Case ID 留存 |
| 分批負載 | 80 requests、8 workers、0 failures；p95 約 0.775 ms |
| 同步負載 | 80 requests、8 workers、0 failures；p95 約 2.098 ms |
| 不合格 p95 門檻 | 正確回傳 exit code 1 |
| 敏感檔案 ignore probes | `.env`、local config、輸出、progress、browser state 均被忽略 |
| 發布候選檔案的來源識別掃描 | 未發現來源公司的名稱、產品代號、內部服務或使用者主目錄路徑 |

負載數字只反映本機測量，不能當作產品 SLA／容量。Word 與 Excel 的測試驗證資料及結構，未宣稱所有輸入都已通過人讀版面 review；正式交付依 artifacts.md 的 render/review 流程。
Jenkinsfile 提供可接入範例，未在遠端 Jenkins instance 執行。真實 API／帳號／設備、產品 contract 與外部 tracker 尚未設定。

## 重現

```sh
python scripts/check_template.py
ruff check .
python -m pytest --run-ui --run-protocol --junitxml=artifacts/junit.xml --results-json=artifacts/results.json
python scripts/export_cases.py qa/examples/catalog-cases.json artifacts/Demo_Readable.xlsx
python scripts/validate_testcases.py artifacts/Demo_Readable.xlsx --warnings-as-errors
python -m qa_demo.load --mode staggered --requests 80 --workers 8
python -m qa_demo.load --mode simultaneous --requests 80 --workers 8
```

Runtime 產物保存在被忽略的 artifacts/，沒有加入模板 Git 歷史。GitHub CI 另驗證 Python 3.11／3.13 及獨立 browser lane，實際結果以該 commit 的 Actions runs 為準。
