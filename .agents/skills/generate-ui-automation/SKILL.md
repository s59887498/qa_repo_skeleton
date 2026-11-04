---
name: generate-ui-automation
description: "把 Reviewed UI 流程與可觀測 locator 轉成 Selenium Page Object 測試及 automation handoff。"
---

# Generate UI Automation

先讀 `automation/AGENTS.md` 與既有 `qa_demo/pages.py`。定位器集中於 Page Object，測試保留行為 assertions。
從實際 DOM/已讀設計找穩定 data-testid、role、label；缺 UI access 時只交 mapping，不臆測 selector。
顯式等待狀態或條件，固定 viewport；UI 與 API 結果需要時交叉驗證。截圖或 visual baseline 需獨立 review，不以 DOM 通過代替。
敏感截圖、storage state 不進 Git。使用 `qa/templates/automation-handoff.md` 記來源、selector gap、測資、cleanup、command 與 evidence。
