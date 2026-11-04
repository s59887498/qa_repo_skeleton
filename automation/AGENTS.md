# Automation 區

沿用根目錄 AGENTS.md。先讀 README 與 `docs/regression-strategy.md`。
- `src/qa_demo/client.py` 負責 HTTP session、timeout、環境驗證；不記錄 request/response body。
- `src/qa_demo/pages.py` 集中 Playwright locator/actions；UI test 使用 auto-retrying `expect` 保留行為 assertion。
- UI 使用 pytest-playwright 的 `page`／`context` fixtures，沿用 `tests/ui/conftest.py` 的 viewport 與 timeout；不在每案自行建立 browser/context。新專案預設 Playwright，既有專案依其框架與遷移授權處理。
- locator 優先 role／label／test ID；不以固定 sleep 或 force click 掩蓋同步問題。後端業務完成另用可觀察條件驗證。
- 每次 run 指定一個 browser，CI 以 matrix 分開；沿用 `docs/ui-playwright.md` 的 trace／截圖指令，附件保存於被忽略的 artifacts/。
- function-scoped `demo_url` fixture 保持資料獨立；真實環境需以 run ID／ownership 隔離並驗證 cleanup。
- 新案例使用 `@pytest.mark.case(id, title, steps=..., expected=...)`；同一 run 的 ID 不重複。
- API smoke、regression、UI、protocol、live、load 分開執行；不得把 opt-in skip 當通過。
- 測試檔不寫死真實環境、帳號、asset ID 或 token。外部 live service 不可退回另一環境。
