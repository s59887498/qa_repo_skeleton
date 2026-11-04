# Demo Catalog — Synthetic Requirements v1

這是模板專用的虛構需求，僅適用本機 demo server。

## DEMO-REQ-001

`GET /health` 回 200 和 `{"status":"ok"}`。

## DEMO-REQ-002

`POST /items` 只有 `X-Demo-Role: editor` 可使用；viewer/guest 回 403。此 header 是測試開關，不是安全登入機制。

## DEMO-REQ-003

body 為 JSON object，name 為字串。去除前後空白後，長度 1–20 可建立；空字串或 21 字元回 422。建立回 201，含不重複 id 與已正規化 name。

## DEMO-REQ-004

`GET /items/{id}` 回同一筆資料；不存在回 404。editor 可以 `DELETE /items/{id}` 清理該筆；刪後讀取回 404。

## DEMO-REQ-005

`/ui` 可輸入名稱並建立項目，顯示「已建立：名稱」，與 API 查得名稱一致。

## DEMO-REQ-006

本機 protocol example 接受 Heartbeat CALL `[2,id,"Heartbeat",{}]`，回同 ID 的 CALLRESULT `[3,id,{"currentTime":UTC}]`。僅示範 envelope/correlation，未宣稱完整 OCPP 相容性。

Case matrix 只示範上述代表路徑，沒有宣稱完整負面／安全／visual／效能覆蓋。新公司需重新依其契約設計。
