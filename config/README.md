# Project Profile

`project.example.json` 是 Agent 與 QA workflow 的非敏感 metadata 格式，複製為 `project.local.json` 後填自己的來源、owner、tracker routing。
pytest live client 直接讀取 `QA_BASE_URL`、`QA_API_TOKEN`、`QA_TIMEOUT_SECONDS` 環境變數，並不自動讀 project profile 或 `.env`。這個區別可避免以填寫 profile 意外觸發 live execution。
本機 demo 忽略所有 live environment settings；新公司的可執行 adapter 若需要 profile loader，應在確認契約後加入並測試未知／缺值行為。
實際公司來源、ID、連結不要寫入 example。若新公司的正式 repo 要版本化非敏感 profile，先明確調整檔名與存取規則。
