# 進度與跨 Agent 交接

每輪專案測試、補測、Bug 複驗、結果更正與報告交付，新增 `operations/progress/<date>_<project>_<run-id>.md`；不覆寫上一輪。使用 `handoff-template.md`。
記錄實際事件時間、時區、記錄時間、環境/build、scope、case IDs、互斥結果、evidence、cleanup、blocker、下一個 owner/action。
只取得局部結果時統計範圍寫 run；全量未知就寫未知。以唯一 Case ID 計數，不把步驟或 HTTP request 數當案例數。
測試完成、報告產出、報告交付及 Release approval 是不同事件，分開記錄。
此模板只保存檔案交接，沒有預設 Dashboard、排程、Asana 同步、通知或自動發布。若未來要接入，依新公司的工具、destination 和明確授權設定。
