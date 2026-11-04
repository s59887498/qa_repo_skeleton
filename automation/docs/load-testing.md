# 壓測範例與接入方式

`python -m qa_demo.load` 自建短生命週期本機服務；不讀 `.env`，不接受外部 URL。每次產物位於唯一 run directory，預設總共 40 requests、4 workers。

| 模式 | 排程 | 示範意義 |
| --- | --- | --- |
| staggered | worker 依序延後啟動，各自執行固定份額 | 漸進增加 concurrency |
| simultaneous | worker 在 barrier 就緒後一起開始 | 同步突發，非分散式絕對同時 |

此 runner 是 closed-loop：每個 worker 等上一筆 response 後才送下一筆。requests/second 是量測值，不是指定 arrival rate；不能直接等同 open-loop 或全系統容量模型。
上限為 2,000 requests、32 workers、每 request 2 秒 timeout；HTTP error／timeout 都保留樣本，沒有自動重試洗掉失敗。p95 使用 nearest-rank，包含失敗樣本。門檻不通過 exit code = 1。
`--p95-ms`、`--max-error-rate` 是此 run 的門檻，範例 500 ms/0% 不代表新公司的 SLA。延遲也包含本機排程／連線建立成本。

接真實服務時另建 adapter，先確認：需求與 SLO、環境 owner、合法測資、rate/concurrency/總量、timeout、停止條件、健康監控、資源隔離、cleanup、上游／下游限制。
若情境是有狀態流程（建立 → 更新 → 結算），驗對應 transaction/resource 的最終狀態與金額單位；不能只看 HTTP 成功。對同一共享設備並行操作需鎖與 owner。
負載 request 數與測試案例數分開。保留原始失敗及補跑結果，不以補跑成功覆蓋第一輪。
