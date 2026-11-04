---
name: organize-testcase-markdown
description: "將既有測試案例整理成可搜尋的 Markdown 索引與單案內容，保留來源 ID、狀態與版本。"
---

# Organize Testcase Markdown

讀本次指定的 Reviewed source；依 project/feature/version 分目錄，保留原 Case ID 與來源版本。
索引包含 ID、title、priority、state、tags、case link；單案包含前置條件、編號步驟與預期、cleanup、source/gap。
搬移或轉格式不改寫已執行結果，不合併不同版本同名案例。索引數量與唯一 ID 對齊；links 必須能解析。
輸出至 `qa/outputs/testcases/<project>/<feature>/markdown/`，以 Markdown 為指定交付物時不額外產 Excel。
