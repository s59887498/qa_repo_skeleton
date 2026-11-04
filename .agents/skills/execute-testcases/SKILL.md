---
name: execute-testcases
description: "依 Reviewed Test Cases 執行測試、保存結果與 evidence、交接 failed cases 及複驗。"
---

# Execute Testcases

先完成 Execution Gate：Reviewed steps、環境/build、access、資料、資源 ownership、cleanup、等待條件、evidence。
每案保存 actual、result、evidence、blocker；未跑保持 Not Started，受阻為 Blocked，刻意排除為 Skipped。不能把收集／登入成功當整案 Passed。
人工使用 Readable View；automation 沿用 runner。UI 文字、DOM、visual、accessibility 各自保留證據。實體要求不能用 simulator 冒充。
Failed 交給 write-bug；複驗記修復版本與新 evidence，不覆寫先前失敗。
結束或暫停依 `operations/README.md` 保存進度摘要；一般 turn 結束後不聲稱能持續輪詢。
