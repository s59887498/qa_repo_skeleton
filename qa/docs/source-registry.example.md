# 需求來源登錄 — Demo Catalog

| ID | 責任面 | 來源 | 版本 | 狀態 |
| --- | --- | --- | --- | --- |
| DEMO-REQ | 本機示範需求 | [catalog-requirements.md](../examples/catalog-requirements.md) | 1 | Synthetic example |
| DEMO-UI | 本機示範 UI | [demo.html](../../automation/src/qa_demo/demo.html) | repo commit | Synthetic example |

新專案填入 PRD、RA、Figma node、OpenAPI、RBAC、版本、owner 與可存取狀態。外部來源只登錄使用者授權的 URL；取得不到內容時記 Source Gap，不當成已讀。
同名來源若版本不同，先處理 Version Mismatch；不同責任面的資訊不宜互相覆蓋。
