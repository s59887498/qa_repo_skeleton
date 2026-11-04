---
name: generate-api-tests
description: "把 Reviewed Cases 與 API contract 轉成既有 pytest client/fixture 的可執行 API 測試。"
---

# Generate API Tests

先讀 `automation/AGENTS.md`、現有 client/fixture 與同 feature 測試。正式程式放 `automation/tests/api/`；live adapter 放明確 opt-in lane。
每案保留 Case ID、title、steps、expected；案例參數化使用單獨 case marker，避免不同案例共用 ID。
驗 status、schema、資料及拒絕後副作用；不只驗 HTTP 200。使用 bounded timeout，真實資料用 run ownership，finally cleanup 並讀回確認。
來源缺 endpoint/auth/contract 時先交 mapping 與 blocker；不得照範例猜新公司 API。命令、環境、evidence、未執行範圍一併交付。
