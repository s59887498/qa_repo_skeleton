# QA Cycle Team

使用者要求整隊協作時，根 Agent 先委派 qa_leader 盤點來源/Gate/Plan/估算，再把獨立 scope 分給 manual_qa 與 automation_qa；兩 lane 回報後 Leader review，根 Agent 整合交付。
每次委派明列檔案 ownership、Case IDs、環境、資料、允許操作及依賴。共用資源需協調；同一檔案、同一測試或同一外部 issue 只有一個 writer。
工具或平台不支援 custom agents 時，可在單一 turn 依同樣角色責任依序工作，不能宣稱已啟動不存在的 Agent。

Handoff Contract：Cycle、Project、Feature、Version、Stage、Gate、Scope、Sources、Inputs、Outputs、Evidence、Defects、Blockers、Risks、Cleanup、Next owner、Next action、External authorization gaps。
Bug 必須使用本次指定的 tracker parent/project。跨時間等待需要真正的排程功能及使用者要求；一般 Agent turn 結束不會自行醒來。
