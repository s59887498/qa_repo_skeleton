# Mode: Test Execution

輸入：Reviewed steps、target profile/build、access/credential reference、測資、ownership、cleanup、timeouts、evidence 方法。
使用 execute-testcases；按逐案 scope 執行，失敗交 write-bug。不具備 access 時留 Blocked 與解除條件。
交付逐案狀態/actual/evidence、缺陷、cleanup、未跑範圍；依 operations/README.md 保存進度。複驗新建 run，不覆寫原始失敗。
