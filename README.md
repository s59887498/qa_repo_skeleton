# QA Repo Skeleton

可帶到下一個專案的 QA 工作底座：AI Agent、Skills、測試設計、文件產生、pytest API／Playwright UI／Protocol 範例、回歸分層、壓測及 CI。

此 repo 不含任何公司的實際需求、帳密、客戶／設備資料、內部服務網址或歷史測試結果。`Demo Catalog` 是虛構的本機示範系統。測試通過只代表模板可運作。

## 5 分鐘試跑

需 Python 3.11+、Git；以下命令都在 repo 根目錄執行。第一次安裝需連公開 PyPI；測試本身預設只用本機 loopback。

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev,documents,protocol]'
python scripts/check_template.py
python -m pytest --run-protocol --junitxml=artifacts/junit.xml --results-json=artifacts/results.json
python -m qa_demo.load --mode simultaneous --requests 40 --workers 4
```

Windows PowerShell 啟用 venv：`.venv\Scripts\Activate.ps1`。未啟用 venv 時可直接使用其 Python 執行檔。

## 結構

```text
.agents/skills/         10 個共用 Skills，含六種 QA workflow mode
.codex/agents/         QA Leader / Manual QA / Automation QA
config/               不含 secrets 的 profile 範例
qa/                   需求入口、方法、格式模板、虛構案例、輸出位置
automation/           pytest、API client、Page Object、本機服務、負載範例
operations/           跨 Agent／跨 turn 的檔案進度交接
scripts/              Excel 匯出／驗證、報告草稿、Word 匯出、模板檢查
tests/                框架與交付工具本身的測試
artifacts/            runtime 產物，預設不進 Git
.github/workflows/    GitHub Actions 的本機範例驗證
Jenkinsfile           Jenkins 起始 pipeline
```

## QA Agent 與 Skills

以這個 repo 根目錄開啟 Codex；新專案需自行信任 workspace，並連接自己的外部工具。模型不寫死，沿用使用者設定。

| 角色 | 責任 |
| --- | --- |
| `qa_leader` | Source/Readiness Gate、Plan、估算、Review、Report/Release 建議 |
| `manual_qa` | Case 設計／執行、evidence、Bug Draft、修復複驗 |
| `automation_qa` | Case mapping、API/UI/Protocol、回歸／壓測、cleanup |

Skills：`qa-workflow`、`generate-test-plan`、`generate-testcases`、`validate-testcases`、`execute-testcases`、`generate-test-report`、`generate-api-tests`、`generate-ui-automation`、`organize-testcase-markdown`、`write-bug`。

可直接貼給 Agent：

```text
使用 $qa-workflow，Mode: Test Case。
來源：qa/examples/catalog-requirements.md；輸出 Readable Excel。
先列 Source Gate 與 coverage map，再產製與驗證案例。
```

```text
啟動完整 QA Cycle；只針對本機 Demo Catalog。
請 qa_leader 先做 Gate，再分派 manual_qa、automation_qa。
交付本機 Test Plan、Test Cases、execution evidence、Bug Draft 與 Test Report。
```

六種 Mode 與 Gate 的唯一入口在 [qa-workflow](.agents/skills/qa-workflow/SKILL.md)。外部 tracker 未設定時只留本機 Bug Draft。
Agent TOML 與 Skills 位置依 [官方 Agent 文件](https://learn.chatgpt.com/docs/agent-configuration/subagents)及 [Skills 文件](https://learn.chatgpt.com/docs/build-skills)配置；平台不支援時可依同樣角色責任依序執行。其他 AI 工具需自行接入這些 Markdown 指令，不宣稱已自動註冊。

## 回歸、UI、Protocol 與壓測

```sh
# 快速 smoke／功能回歸；額外 lane 明確選入
python -m pytest -m smoke
python -m pytest -m 'regression and not ui'

# Playwright UI：安裝套件與配對瀏覽器，失敗保留 trace／截圖
python -m pip install -e '.[ui]'
python -m playwright install chromium
python -m pytest automation/tests/ui --run-ui --browser chromium \
  --tracing retain-on-failure --screenshot only-on-failure \
  --output artifacts/ui/chromium/playwright \
  --junitxml=artifacts/ui/chromium/junit.xml --results-json=artifacts/ui/chromium/results.json

# 最小 OCPP-J Heartbeat request/response 範例，只連本機
python -m pytest automation/tests/protocol --run-protocol

# 分批啟動與同步啟動，預設 p95 <= 500 ms、error rate = 0
python -m qa_demo.load --mode staggered --requests 80 --workers 8
python -m qa_demo.load --mode simultaneous --requests 80 --workers 8
```

UI optional dependencies 不存在或配對瀏覽器未安裝時，明確選入的 lane 會失敗；不悄悄當作成功。預設 skip 的 live/UI/protocol 不算 Passed。
新 UI 專案預設 Python＋pytest＋Playwright；既有專案先沿用其框架。每 run 選一個 browser，GitHub CI 分別執行 Chromium／Firefox／WebKit。單獨加 `--run-ui` 只會啟用測試，錄製與截圖由上列 flags 控制。
壓測的 error rate、p50/p95、RPS 及逐筆結果寫入 `artifacts/load/<run-id>/`。這是可重用的負載組織範例，不是任何產品的效能承諾；遠端壓測需另接 adapter 與確認 SLO/授權。

詳細說明：[Automation](automation/README.md)、[Playwright UI 與 evidence](automation/docs/ui-playwright.md)、[回歸分層](automation/docs/regression-strategy.md)、[負載模型](automation/docs/load-testing.md)。

## Test Case 與 Report

```sh
python scripts/export_cases.py qa/examples/catalog-cases.json artifacts/Demo_Readable.xlsx
python scripts/validate_testcases.py artifacts/Demo_Readable.xlsx --warnings-as-errors
python scripts/build_report.py artifacts/results.json artifacts/report.md
python scripts/export_docx.py artifacts/report.md artifacts/report.docx
python scripts/export_docx.py qa/templates/test-plan.md artifacts/plan-template.docx
```

Excel 保留 `README_使用說明`、`Case Index`、`Readable View` 三張表；Word 保留七章測試計劃／報告的內容架構。新產物是 Draft，正式交付需依 [文件規則](docs/artifacts.md) 檢查來源、內容與版面。
所有工具只依輸入產生本機檔案，不自動發布、寄信、開 Bug 或覆寫外部工作簿。

## 接入下一個專案

1. 用此 repo 建立獨立的新專案；不要把公司資料回推到通用模板。
2. 複製 `config/project.example.json` 為 `config/project.local.json`，填 project、source registry、owner、tracker destination。
3. 登錄新公司的 PRD／RA／UI／OpenAPI／RBAC 來源與版本；建立自己的產品 Skill／adapter。
4. 使用環境變數或本機 `.env` 保存 credentials。範例不讀取 `.env`，也不會自動套用舊環境。
5. 先驗本機範例，再逐項接入新 API、locator、測資、cleanup 與 live execution 範圍。

唯讀 live 範例（須先核對目標確實有 `/health` contract）：

```sh
cp .env.example .env
# 編輯自己的本機 .env 後，僅在你信任該檔案時載入
set -a
. ./.env
set +a
python -m pytest automation/tests/live --run-live
```

未填 `QA_BASE_URL` 會失敗；沒有跨環境 fallback。有 token 時要求 HTTPS。不要將 secrets 填進命令歷史、README 或 project example。

完整接手清單見 [移轉指南](docs/migration.md) 與 [能力移轉對照](docs/capability-map.md)。此模板未選定開源授權；若要公開散布，維護者應自行決定授權條款。
