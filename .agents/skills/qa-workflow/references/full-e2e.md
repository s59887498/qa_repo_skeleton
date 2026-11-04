# Mode: Full E2E

先列使用者要求的 Expected Output；重用已合格的 Plan/Cases，不無條件重做。
依 Source → Design/Automation → Execution → Report 逐階段 Gate。未來尚未產生的 evidence 不阻擋前面階段。
跨角色時依 team.md 委派；源文件 qa/、可執行程式 automation/、進度 operations/。
以 Case ID 串聯需求、手動/自動化、結果、Bug、複驗、報告。只有實測完成的部分可寫 Passed；留下未測與 blocker。
最終由根 Agent 整合所有 lane，核對重複 ID、ownership、cleanup 與交付狀態。
