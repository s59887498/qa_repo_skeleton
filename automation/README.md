# Automation Framework

從 repo 根目錄執行，依根 README 安裝 Python 套件。`qa_demo` 以 editable package 安裝，不依賴個人路徑或 `sys.path` hack。

| 位置 | 用途 |
| --- | --- |
| `src/qa_demo/client.py` | HTTP client、timeout、LiveSettings、無跨環境 fallback |
| `src/qa_demo/server.py` | 每案獨立的 synthetic loopback 目標，thread-safe data |
| `src/qa_demo/pages.py` | Selenium Page Object／locator／explicit waits |
| `data/catalog.json` | 非敏感角色與 boundary 參數 |
| `tests/api/` | 功能、權限、邊界、owned cleanup 範例 |
| `tests/ui/` | UI 建立後讀回 API；不是 visual baseline 驗證 |
| `tests/protocol/` | 最小 Heartbeat envelope／correlation 範例 |
| `tests/live/` | opt-in 唯讀接入點，缺設定會失敗 |
| `src/qa_demo/load.py` | 有上限的分批／同步負載及 p95/error-rate gate |

所有 automation cases 使用 `@pytest.mark.case` 保留 ID、title、steps、expected；重複 ID 在 collection 時拒絕。
根 `conftest.py` 會保存 execution JSON；setup/teardown 失敗不能被 call 階段 Passed 蓋掉。詳細錯誤仍查 JUnit／console，分享前先去敏。

```sh
python -m pytest --junitxml=artifacts/junit.xml --results-json=artifacts/results.json
python -m pip install -e '.[reports]'
python -m pytest automation/tests/api --alluredir=artifacts/allure-results
```

Allure CLI 是選用工具，另由新公司安裝；Python plugin 只產 raw results。Allure/JUnit 中可能含 assertion context，對真實環境使用時需遵守公司的 artifact 存取與保留規則。
Chrome driver 可用 `QA_CHROMEDRIVER` 指向已安裝檔案，`QA_CHROME_BINARY` 指定 browser，避免自動下載。這些設定只存本機。
Jenkinsfile 是 pipeline 起點，未連接任何 Jenkins instance；GitHub Actions 預設只跑 synthetic local examples，沒有 production secrets、通知或 deployment。
