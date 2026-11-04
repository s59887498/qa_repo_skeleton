# 模板驗證紀錄

驗證日期：2026-11-04。驗證範圍為此模板的 synthetic examples 與工具，不是任何公司的產品測試。

## Playwright 切換驗證

版本：Python 3.14.3、pytest 9.2.0、Playwright 1.64.1、pytest-playwright 0.10.0。UI 套件已切換，模板 venv 不再安裝 Selenium。

| 項目 | 結果 |
| --- | --- |
| 完整回歸＋Chromium UI＋WebSocket | 34 passed、1 skipped；skip 是未啟用的 live lane |
| Firefox UI／附件整合檢查 | 2 passed |
| WebKit UI／附件整合檢查 | 2 passed |
| 失敗附件政策 | 三種 browser 均驗證：刻意失敗留下可讀 trace ZIP／PNG；成功不保留 |
| Case ID／結果整合 | UI 與 API 資料一致；JSON 記 browser，Allure 保留 ID／標題／steps／expected |
| Optional UI 與分 run 規則 | 無 plugin 的 core run 可用；明確要求 UI 卻缺 plugin 會失敗；同次多 browser 會提示分開執行 |
| Skill／語法／文件連結／Ruff | 通過 |

本機 pytest 9.2 對上游 plugin 的 session-scoped `base_url` fixture 顯示一筆 deprecation warning；測試通過，套件範圍仍限制 pytest < 10。沒有隱藏 warning 或修改第三方套件。
Jenkins UI stage 已加入，但未在真實 Jenkins instance 執行。GitHub CI 設定為兩個 Python core jobs 與三個 browser jobs，實際狀態以該 commit 的 Actions runs 為準。

## 初始模板驗證（保留紀錄）

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
python -m playwright install chromium
python -m pytest --run-ui --run-protocol --browser chromium \
  --tracing retain-on-failure --screenshot only-on-failure \
  --output artifacts/ui/chromium/playwright \
  --junitxml=artifacts/junit.xml --results-json=artifacts/results.json
python scripts/export_cases.py qa/examples/catalog-cases.json artifacts/Demo_Readable.xlsx
python scripts/validate_testcases.py artifacts/Demo_Readable.xlsx --warnings-as-errors
python -m qa_demo.load --mode staggered --requests 80 --workers 8
python -m qa_demo.load --mode simultaneous --requests 80 --workers 8
```

Runtime 產物保存在被忽略的 artifacts/，沒有加入模板 Git 歷史。完整安裝與跨瀏覽器指令見 [UI 指南](../automation/docs/ui-playwright.md)。
