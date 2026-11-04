# 新公司／新專案接手清單

## 取用模板

用 GitHub 建立新 repo 後把模板檔案放入，或自行複製此 repo 的 working tree。將新公司的 remote 設為新 repo；不要將公司後續資料推回這份通用模板。
若 repository owner 啟用 GitHub 的 Template repository 設定，即可用 Use this template；本次只提供模板內容，不假設該管理設定已啟用。

## 需要重新設定

- `config/project.local.json`：project、owner、timezone、source registry、環境與 tracker destination。example 僅作結構，不直接當 live 設定。
- `.env`／secret manager：API base URL、token、帳號、瀏覽器／driver 路徑；不複製舊 `.env` 或 shell history。
- `qa/docs/`：新 PRD、RA、UI/Figma、OpenAPI、RBAC、版本；不搬舊公司的真實規格與圖片。
- `automation/`：API adapter、authentication、selector、測資與 cleanup；先以新契約建 mapping，再接真實環境。
- Bug routing：Asana/Jira/GitHub provider、project、parent、section，保留空白直到本次指定。若需 connector，使用自己的登入與 permission。
- CI：runner、Python、套件來源、artifact retention、secret scope、live job；預設 CI 沒有排程與真實環境執行。
- Agent：從新 repo root 開啟，確認三個 roles 與十個 Skills 可用。MCP credentials、app plugins、個人 Codex config 需各自設定，並未打包。
- 文件：公司格式、簽核、字型、metadata、輸出可見性；視需要調整 qa/templates 與 exporter。

## 接入驗證順序

1. 安裝並跑模板檢查、local regression、protocol、文件工具測試。
2. 啟用 UI lane，確認 browser／driver 與本機範例。
3. 補新來源與 project profile，先做 Source Gate 和 Test Plan／Cases。
4. 已確認契約且授權後才跑 live read-only smoke；核對 token 不會跨環境。
5. 建立隔離測資與 owned cleanup，再接 mutation regression／壓測。
6. 產出真實 evidence，保存進度與報告。例行排程、通知、部署另依需求設定。

## 移轉邊界

保留方法、角色、技能與交付格式；環境特定的程式重寫成 synthetic examples，沒有複製原始 Git objects/history。
不帶公司／產品名稱、內部 domain、個人主目錄路徑、真實 project ID、來源連結、客戶/員工資料、設備清單、歷史報告、截圖、排程、憑證或舊授權。
內部 Dashboard 與 domain-specific business rules 改成進度 handoff contract 與 project profile 接入點；本模板不附舊工作台／資料／部署設定。
發布前跑 `python scripts/check_template.py` 並人工 review `git diff --cached`。通用掃描可找明顯 token／內部連結／路徑，但新公司的詞彙仍需維護者核對。
