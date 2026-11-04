---
name: generate-ui-automation
description: "把 Reviewed UI 流程與可觀測 locator 轉成可追溯的 UI 自動化及交接；新專案預設 Playwright，既有專案沿用其框架。"
---

# Generate UI Automation

先讀 `automation/AGENTS.md`、`automation/docs/ui-playwright.md` 與既有 `qa_demo/pages.py`。新專案預設 Python＋pytest＋Playwright；已有框架先沿用，依使用者指定範圍執行遷移。
此模板使用 pytest-playwright 管理的 page/context fixtures；Page Object 集中 locator/actions，測試用 auto-retrying `expect` 驗證行為。自行建立 context 會繞過 fixture 的 CLI 附件設定，確有需要時必須另外接上 lifecycle/evidence。
從實際 DOM 找 role、label、test ID；設計文件僅作行為與文案來源。缺 UI access 時交 mapping，不臆測 selector。使用 bounded timeout 與條件等待，不以固定 sleep、force click 或重跑掩蓋失敗。
固定 viewport；UI 與 API 結果需要時交叉驗證，auto-wait 不代表後端業務已完成。每 run 選一個 browser，跨瀏覽器分 run/CI job 保存，保留 Case ID 與 browser evidence。
依 UI 指南設定 `--tracing retain-on-failure`、`--screenshot only-on-failure` 與被忽略的 artifact output；實際確認附件後才列為 evidence。截圖或 visual baseline 需獨立 review，不以 DOM 通過代替。
trace、敏感截圖、storage state 不進 Git。使用 `qa/templates/automation-handoff.md` 記來源、selector gap、測資、cleanup、browser、command 與 evidence。
