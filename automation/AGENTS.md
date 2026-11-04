# Automation 區

沿用根目錄 AGENTS.md。先讀 README 與 `docs/regression-strategy.md`。
- `src/qa_demo/client.py` 負責 HTTP session、timeout、環境驗證；不記錄 request/response body。
- `src/qa_demo/pages.py` 集中 locator 與顯式等待；UI test 保留行為 assertion。
- function-scoped `demo_url` fixture 保持資料獨立；真實環境需以 run ID／ownership 隔離並驗證 cleanup。
- 新案例使用 `@pytest.mark.case(id, title, steps=..., expected=...)`；同一 run 的 ID 不重複。
- API smoke、regression、UI、protocol、live、load 分開執行；不得把 opt-in skip 當通過。
- 測試檔不寫死真實環境、帳號、asset ID 或 token。外部 live service 不可退回另一環境。
