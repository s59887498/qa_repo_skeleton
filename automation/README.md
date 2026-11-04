# Automation Framework

從 repo 根目錄執行，依根 README 安裝 Python 套件。`qa_demo` 以 editable package 安裝，不依賴個人路徑或 `sys.path` hack。

| 位置 | 用途 |
| --- | --- |
| `src/qa_demo/client.py` | HTTP client、timeout、LiveSettings、無跨環境 fallback |
| `src/qa_demo/server.py` | 每案獨立的 synthetic loopback 目標，thread-safe data |
| `src/qa_demo/pages.py` | Playwright Page Object／role、label locator／actions |
| `data/catalog.json` | 非敏感角色與 boundary 參數 |
| `tests/api/` | 功能、權限、邊界、owned cleanup 範例 |
| `tests/ui/` | plugin-managed page/context、固定 viewport；UI 建立後讀回 API |
| `tests/protocol/` | 最小 Heartbeat envelope／correlation 範例 |
| `tests/live/` | opt-in 唯讀接入點，缺設定會失敗 |
| `src/qa_demo/load.py` | 有上限的分批／同步負載及 p95/error-rate gate |

所有 automation cases 使用 `@pytest.mark.case` 保留 ID、title、steps、expected；重複 ID 在 collection 時拒絕。
根 `conftest.py` 會保存 execution JSON；setup/teardown 失敗不能被 call 階段 Passed 蓋掉。詳細錯誤仍查 JUnit／console，分享前先去敏。
UI 的 JSON／JUnit 記錄 browser；每 run 只選一個 browser，以保留唯一 Case ID。Trace 與截圖在 Playwright output directory，JSON 的錄製政策與路徑不保證附件已產生。

```sh
python -m pytest --junitxml=artifacts/junit.xml --results-json=artifacts/results.json
python -m pip install -e '.[reports]'
python -m pytest automation/tests/api --alluredir=artifacts/allure-results
```

Allure CLI 是選用工具，另由新公司安裝；Python plugin 只產 raw results。Allure/JUnit 中可能含 assertion context，對真實環境使用時需遵守公司的 artifact 存取與保留規則。
UI 安裝、跨瀏覽器、trace 與離線 cache 見 [Playwright 指南](docs/ui-playwright.md)。套件安裝後需另執行 `python -m playwright install chromium`；升級 Playwright 後要重新安裝對應瀏覽器。
Jenkinsfile 含 Chromium UI stage；Linux agent 須先備妥瀏覽器系統函式庫，可由管理者執行 `python -m playwright install-deps chromium`。此 pipeline 尚未連接任何 Jenkins instance。
GitHub Actions 以獨立 matrix jobs 執行 Chromium／Firefox／WebKit，並用 `install --with-deps` 安裝對應瀏覽器與 Linux dependencies；只跑 synthetic local examples，沒有 production secrets、通知或 deployment。
