---
name: validate-testcases
description: "檢查 Readable Excel 的 Case ID、索引對照、步驟、狀態與基本 traceability，適用於 Review 和交接前。"
---

# Validate Testcases

執行 `python scripts/validate_testcases.py <path.xlsx> --warnings-as-errors`。
檢查必要 sheets/columns、ID 唯一、Index/Readable 對應、Step # 正整數連號、Step Count、非空 steps/expected、Priority/State/Tags。
canonical implementation：`scripts/validate_testcases.py`，不要另造不一致的 validator。
ERROR 先修；來源不明不能以虛構需求消除 warning。格式 validator 不證明覆蓋充分、行為正確或已實跑。
