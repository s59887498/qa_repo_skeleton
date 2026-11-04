# QA 文件區

沿用根目錄 AGENTS.md。需求存 docs/；templates/ 是格式；examples/ 是虛構示範；outputs/ 是當次產物。
產製前決定 `qa/outputs/<plans|testcases|reports|bugs>/<project>/<feature>/`，避免產品、版本或測試輪次混放。
來源依責任面交叉核對：PRD 商業行為、RA 決策、UI 可見介面、API contract、RBAC 權限。沒有全域單一優先序。
人讀標題、步驟、預期結果用繁中；ID、API path、env var 保留原名。每個步驟要能實際操作並對應可觀測結果。
案例與報告僅聲稱有證據的範圍；partial rerun 不覆蓋全量狀態。格式及產生指令見 README。
