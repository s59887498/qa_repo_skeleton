---
name: generate-test-report
description: "依實際執行結果及缺陷產出測試報告，區分局部結果、未測範圍與 Release 建議。"
---

# Generate Test Report

依 qa-workflow 的 Test Report Mode，彙整實際 test results、defects、cleanup 與 limitations。
採用 `qa/templates/test-report.md`；pytest 的 `--results-json` 可交給 `python scripts/build_report.py <results.json> <report.md>` 產生草稿。
生成器只彙整本次 run，不能自動證明 project completion 或 release approval。人工補上來源、build、未測範圍、缺陷、交付及簽核。
Case ID 去重，Passed/Failed/Blocked/Skipped/Not Started 互斥；沒有 evidence 不填 Passed。測試步驟與壓測 request 不等於 Case count。
需要 Word 時執行 `scripts/export_docx.py`，依 `docs/artifacts.md` 渲染後 review。交付後留下 operations 進度檔。
