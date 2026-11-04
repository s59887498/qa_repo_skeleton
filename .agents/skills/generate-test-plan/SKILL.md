---
name: generate-test-plan
description: "依需求及已確認來源產出測試計劃、範圍、估算與 Readiness，使用於 Test Plan 交付。"
---

# Generate Test Plan

依 qa-workflow 的 Test Plan Mode 工作。來源限定本次 project/feature/version。
以 `qa/templates/test-plan.md` 產出 `qa/outputs/plans/<project>/<feature>/`；有既有格式先沿用。
風險對應範圍、技法、evidence lane、測資、cleanup、owner；估算用區間並列假設和依賴。
缺 runtime credentials 不阻擋策略設計；缺需求／決策則標受影響範圍與待確認 owner。
Word 格式可將 Markdown 交給 `scripts/export_docx.py`，交付前依 `docs/artifacts.md` 做 render/review。
