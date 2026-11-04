---
name: qa-workflow
description: "依六種模式協調測試計劃、案例、執行、自動化、報告與完整 QA Cycle；模板維護與局部修正不自動啟用。"
---

# QA Workflow

本 Skill 的程式路徑從 repo 根目錄解析；Markdown reference 連結從本檔解析。先讀根 AGENTS.md 與 project profile。

| Mode | 目的 | Reference |
| --- | --- | --- |
| Test Plan | 範圍、策略、估算 | [test-plan](references/test-plan.md) |
| Test Case | 設計與 Review | [test-case](references/test-case.md) |
| Test Execution | 依 Reviewed Cases 執行 | [test-execution](references/test-execution.md) |
| Automation | 實作或執行 API/UI/Protocol | [automation](references/automation.md) |
| Test Report | 彙整實際 evidence | [test-report](references/test-report.md) |
| Full E2E | 多階段需求到交付 | [full-e2e](references/full-e2e.md) |

選定 Mode 後只讀該 reference 與 [readiness](references/readiness.md)。多來源設計讀 [source-gate](references/source-gate.md)；明確要求 QA Team 時讀 [team](references/team.md)。
Gate 只有 PASS、PARTIAL、BLOCK；說明可繼續、受阻範圍與下一動作。缺 runtime access 不阻擋設計；沒有 execution evidence 不產 Final Report。
交付前檢查 [output-contract](references/output-contract.md)。只產出使用者指定交付物，不擅自建立排程、通知或發布。
