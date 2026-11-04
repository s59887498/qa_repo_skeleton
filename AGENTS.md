# QA Workspace — Agent Rules

這是可移植的單一模板 repo。`qa/` 保存來源、測試設計與文件；`automation/` 保存可執行測試；`operations/` 保存進度交接。所有 repo reference 使用相對路徑。

- Test Plan、Test Case、Test Execution、Automation、Test Report、Full E2E：先讀 `.agents/skills/qa-workflow/SKILL.md` 並只載入選定 Mode reference。局部腳本修改與模板維護不需啟動完整 QA 流程。
- 單一 Bug 交付物使用 `.agents/skills/write-bug/SKILL.md`。只有使用者已授權且指定 tracker destination 時才寫外部系統；未設定時保留本機 Draft。
- 先讀 `config/project.example.json` 的格式與本次 project profile；實際環境設定存 `config/project.local.json`。範例不是新公司的產品規格。
- 不憑空建立需求、API path、permission、預期結果或執行證據。來源缺漏、衝突、版本不符分開記錄。缺憑證只阻擋執行，不阻擋可完成的測試設計。
- 帳密、JWT、Token、個資、設備清單、付款資料與登入 state 不進 Git。用環境變數或被忽略的本機設定；`.env` 不自動載入，見 README。
- `automation/tests/` 的案例沿用 client、fixtures、Page Object、case metadata。預設只跑 synthetic local examples。live execution 與壓測範圍依本次使用者授權，不能繼承來源公司的歷史授權。
- 新專案的 UI automation 預設 Python＋pytest＋Playwright；接手已有框架的專案時先沿用其選型，技術遷移依使用者指定範圍。此模板使用 plugin-managed page/context 與失敗附件設定，見 `automation/docs/ui-playwright.md`。
- 只清理本輪擁有的資源。真實系統的破壞性／不可逆行為須有對應授權；讀取設定本身不代表獲准執行。
- 專案測試／複驗的可交接點，依 `operations/README.md` 新增進度檔。框架單元測試不冒充產品測試。
- 使用者要求完整 QA Cycle 或三個角色協作時，根 Agent 先委派 `qa_leader` 做 Gate，再依範圍分派 `manual_qa`、`automation_qa`，最後回 Leader review；遵守 `.agents/skills/qa-workflow/references/team.md`。單一交付物不強制拆分。
- 同一檔案／外部 task 同時間只有一個 writer。工作中不得撤銷其他人的變更。每次交接包含 Gate、outputs、evidence、defects、blockers、next owner/action。
