# 回歸測試怎麼寫、怎麼分

保留「feature 分模組、case ID 可追溯、環境與 assertion 分離、分層選跑」的結構。

| Suite | 內容 | 範例指令 | 建議觸發 |
| --- | --- | --- | --- |
| Smoke | 服務／關鍵入口 | `python -m pytest -m smoke` | 每次變更 |
| API regression | 行為、schema、RBAC、boundary、lifecycle | `python -m pytest automation/tests/api` | PR／回歸 |
| UI | 操作及跨層資料一致性 | `python -m pytest automation/tests/ui --run-ui` | UI 變更／nightly |
| Protocol | message envelope、correlation、timeout | `python -m pytest automation/tests/protocol --run-protocol` | protocol 變更 |
| Live read-only | 已確認 target 的健康檢查 | `python -m pytest automation/tests/live --run-live` | 明確授權時 |
| Load | request 總量、並行、延遲／錯誤率 | `python -m qa_demo.load` | 獨立效能任務 |

本模板只設定 push/PR CI，沒有自動建立 nightly schedule。

新增 feature：先有 Reviewed Cases 與 source registry，再放 `automation/tests/api/test_<feature>_regression.py`；可重用 client／helper 放 src，測資放 data，真實 asset ID 放 local config。
每組參數是獨立案例時，使用 `pytest.param(..., marks=pytest.mark.case(...))` 保持不同 ID。Title 短且人可讀，steps/expected 分欄；不把整段 payload 塞到報表標題。
測試先 Arrange，再 Act，最後 Assert；assert status 以外還驗 data/permission/side effects。清理只限該 run 建立的資料；多環境共用 assertion，credentials/config 隔離且缺值不能退回其他環境。
live suite 不能因 access 不足被誤算 Pass。與實體硬體／人工判斷有關的部分列明 limitation；本機 protocol example 不代表充電端到端或認證通過。
