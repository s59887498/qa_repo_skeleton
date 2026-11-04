---
name: generate-testcases
description: "由已確認需求設計可執行、可追溯的繁中測試案例，輸出 Readable Excel 或指定格式。"
---

# Generate Testcases

依 qa-workflow 的 Test Case Mode 與 `qa/methodology/test-design.md` 建立 design map，範例在 `qa/examples/catalog-cases.json`。
每案至少有 id/title/module/priority/source/preconditions/tags/steps/cleanup；每一步含 action 與 expected。ID 唯一；priority 為 High/Medium/Low；State 初始 Not Started。
來源缺少規則、boundary、permission 或 API path 時，不補造精確 assertion；在 notes 保留 Source Gap。
JSON 是此模板的機器來源；`python scripts/export_cases.py <cases.json> <Readable.xlsx>` 產出 README_使用說明、Case Index、Readable View。
主執行文件是 Readable View，每步都能單獨操作並看出結果；Case Index 僅作 scope 索引。前置條件與 cleanup 需包含在輸出。
執行 `python scripts/validate_testcases.py <Readable.xlsx> --warnings-as-errors`；格式通過後仍需確認語意／來源，不宣稱自動完成 review。
參見 `docs/artifacts.md` 的人讀交付檢查。
