# Playwright UI

本模板的新 UI automation 使用 Python＋pytest＋pytest-playwright。接手已有測試框架的專案時，先沿用其選型；依使用者指定的範圍做遷移。

## 安裝與執行

從 repo 根目錄與已啟用的 venv 執行：

```sh
python -m pip install -e '.[ui,reports]'
python -m playwright install chromium
python -m pytest automation/tests/ui --run-ui --browser chromium \
  --tracing retain-on-failure --screenshot only-on-failure \
  --output artifacts/ui/chromium/playwright \
  --junitxml=artifacts/ui/chromium/junit.xml \
  --results-json=artifacts/ui/chromium/results.json \
  --alluredir=artifacts/ui/chromium/allure-results
```

`--run-ui` 只啟用測試，trace／截圖由上面的 flags 控制。預設 headless；調試可加 `--headed`。缺 plugin 或 browser 時明確失敗，不轉成 Passed 或偷偷改用另一套工具。
每個 run 只選一個 browser，避免相同 Case ID 在同份結果重複。Firefox／WebKit 分別執行 `python -m playwright install firefox`／`webkit`，將上面 browser 與輸出目錄一起替換。不要同次傳入多個 `--browser`；GitHub CI 已用三個獨立 matrix jobs。

## Fixture 與寫法

- 使用官方 `page`／`context` fixtures；每案獨立 context，session browser 由 plugin 管理。這讓 CLI trace、截圖與 context cleanup 一致生效。
- `tests/ui/conftest.py` 固定 1440×900 viewport，操作 timeout 5 秒、navigation timeout 10 秒。必要調整集中在 fixture。
- `CatalogPage` 集中 role／label locators 與 actions。使用 `get_by_role`、`get_by_label` 或穩定 test ID，避免綁死 DOM 層級。
- 操作由 Playwright auto-wait；測試使用 `expect(locator).to_have_text(...)` 等自動重試 assertion。後端訂單、任務或結算狀態需另有明確完成條件與 timeout。
- 範例以 UI 建立項目後讀回 API，比對同一 item ID 與名稱。Page Object 不替測試隱藏 assertion；不使用固定 sleep、force click 或無上限重跑。

若自行呼叫 `browser.new_context()`，CLI 附件設定不會自動套用；需要新增角色/context 時優先使用 plugin 支援的 fixture，並驗證其 evidence lifecycle。登入 state 存在被忽略的 `playwright/.auth/` 或本機設定，不能提交憑證。

## Evidence 與報告

失敗案例的 trace ZIP 與 PNG 保存在 `--output` 下，以 test node/browser 分資料夾；成功案例不保留這些失敗附件。可用 `python -m playwright show-trace <trace.zip>` 在本機檢視。
Case ID、標題、steps/expected 保留於 Allure；JSON／JUnit 記錄 browser，報告草稿列出 capture policy 與 output directory。Playwright trace／截圖獨立保存，不宣稱已自動附入 Allure。
`tests/test_playwright_integration.py` 會在隔離目錄執行一個預期成功與一個刻意失敗的 synthetic browser test，驗證成功不留附件、失敗留下可讀 trace／PNG、Case ID 與 failure status 正確；外層測試會在這些條件成立時通過。

trace 可能含 DOM、網路資訊與頁面資料；與截圖、影片、登入 state 一樣不進 Git。CI 目前只有 synthetic local data，artifact 保存 7 天；接真實環境前依專案規則配置存取權與去敏。`--output` 由 plugin 管理，不用同一資料夾保存其他長期證據。

## CI 與離線環境

GitHub Actions 安裝套件後執行 `python -m playwright install --with-deps <browser>`。Jenkins 範例使用 Chromium；Linux agent 的 OS dependencies 由管理者先安裝，再由 job 安裝配對 browser。
套件升級後重新安裝 browser。離線執行需預先準備相同 Playwright 版本的 browser cache；可透過 `PLAYWRIGHT_BROWSERS_PATH` 指定，安裝與執行必須使用同一設定。不要把 browser binaries 放進 Git。

參考：[pytest plugin](https://playwright.dev/python/docs/test-runners)、[auto-wait／assertions](https://playwright.dev/python/docs/actionability)、[CI](https://playwright.dev/python/docs/ci)、[browser 安裝](https://playwright.dev/python/docs/browsers)。
