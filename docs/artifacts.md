# 文件產生與交付規則

目前模板以文字／JSON 維護，避免二進位模板夾帶舊作者、revision、hidden sheets 或公司 logo。Excel／Word 由可讀程式生成。

## Readable Excel

`scripts/export_cases.py` 接收 `qa/examples/catalog-cases.json` 同型資料：cases array，每案 id/title/module/priority/source/preconditions/tags/steps/cleanup，steps 有 action/expected；notes 可選。
初始化 State 固定 Not Started。三張表為 README_使用說明、Case Index、Readable View；Step # 從 1 連號，Step Count 對齊；來源文字強制以字串寫入，避免 formula injection。
validator 檢查資料結構與對應，不能判斷產品語意。正式交付前在 Excel／LibreOffice 檢查完整中文、換行、可讀欄寬、列高、列印範圍與步驟可執行性。極長文字需另調欄寬列高。

## Test Plan / Test Report Word

Markdown 模板有七個章節。`scripts/export_docx.py` 支援基本標題、段落、項目及 Markdown tables，不是完整 Markdown renderer；保留 seven-section 內容，不依賴舊公司的二進位資產。
Word 可用的繁中字型由環境決定；範例設定 Noto Sans CJK TC，缺字型時需安裝或改成公司核准字型。
正式交付：先核對來源／統計，再用 Word／LibreOffice 或環境提供的 render 工具轉 PDF/PNG，逐頁看表格跨頁、斷字、頁邊界、標題與頁碼；有問題再調整後重看。只通過程式結構測試不能宣稱已完成版面驗收。

## 執行報告

`--results-json` 的每案含 case_id/title/status/actual/evidence/lane；scope 為 run。Passed/Failed 必須有 evidence，重複 ID 必須人工核對合併規則後處理。
本機 generator 只產 Draft。需補 build、owner、source version、缺陷、cleanup 與未測限制後才做 Final Review。結果 JSON、JUnit、Allure、截圖與 Word 預設不進模板 Git。
