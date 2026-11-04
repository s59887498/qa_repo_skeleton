# Mode: Automation

輸入：Reviewed Cases、contract、既有 framework、環境/資料/cleanup。先盤點相同 client/fixture/Page Object，按 API/UI/Protocol 分 lane。
API 使用 generate-api-tests；UI 使用 generate-ui-automation；protocol 依已確認契約擴充本機示範。
產出 mapping/scaffold 不等於 live Pass。缺環境時仍可做 isolation tests；實跑前另確認授權與 Execution Gate。
壓測先定 workload（ramp/simultaneous）、總量/並行上限、timeout、停止條件、SLO、資源與清理。不要把範例門檻帶入產品 SLA。
