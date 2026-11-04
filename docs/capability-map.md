# 能力移轉對照

以下對照說明抽取的是哪些工作能力；不攜帶來源公司的名稱、repo URL 或歷史業務資料。

| 原工作區能力 | 模板位置 | 移轉方式 |
| --- | --- | --- |
| Parent AGENTS 與 repo 分工 | AGENTS.md、qa/、automation/、operations/ | 重寫通用規則；建立獨立 Git 歷史 |
| 三個 QA custom agents | .codex/agents/ | 保留角色與 handoff，移除產品規則及舊授權 |
| 六種 QA Mode、Gate、Source Review | .agents/skills/qa-workflow/ | 通用化條件與輸出契約 |
| Plan／Case／Report／Bug 等專用 Skills | .agents/skills/ 下其餘 9 個 skills | 保留方法與格式，改用可攜路徑 |
| Readable workbook validator | scripts/validate_testcases.py | 選取無公司依賴的實作，修正分數步驟、空數量及空輸入檢查 |
| 測試設計技法與 evidence lane | qa/methodology/test-design.md | EP/BVA/DT/ST/UC 核心方法通用摘要 |
| Test Case Excel 與 Word 報告 | qa/templates/、scripts/ | 以文字來源生成，移除舊 binary metadata |
| API/UI 回歸框架 | automation/src/、automation/tests/ | 保留 fixture/client/Page Object/metadata 分層，重寫 synthetic 範例 |
| 跨環境回歸 | LiveSettings、tests/live/ | 明確設定、opt-in，不 fallback 或保留服務位址 |
| Protocol harness | tests/protocol/ | 最小本機 OCPP-J correlation 示範；未搬完整業務模擬器 |
| 分批／同步壓測與報表 | qa_demo/load.py | bounded local workload、逐筆 evidence、p95/error gate |
| pytest/Jenkins/Allure/CI | pyproject.toml、Jenkinsfile、.github/ | 通用 pipeline，無公司 runner／通知／排程 |
| 進度摘要／跨模型交接 | operations/ | 保留檔案 handoff；不攜帶工作台及歷史資料 |
| 專屬產品 Skill／tracker routing | config/project.example.json | 改為空白接入點，等新需求填入 |

`Demo Catalog`、Case IDs、角色、名稱長度 1–20 與 localhost server 都是重新撰寫的示範，不代表任何原公司系統。
