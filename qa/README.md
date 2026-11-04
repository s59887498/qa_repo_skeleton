# QA 文件工作區

`docs/` 登錄新專案需求來源；`methodology/` 保存通用設計方法；`templates/` 保存交付格式；`examples/` 全部是 synthetic demo；`outputs/` 才是當次交付物。
使用步驟與指令見根 [README](../README.md)；六種模式由 `.agents/skills/qa-workflow/` 統一管理。
設計 JSON → Readable Excel → validator；實際 execution JSON → report draft → Word export。生成器不代替需求 review、實測或簽核。
新公司自有文件／成果預設被忽略，請在正式公司 repo 明確決定哪些允許版本化，避免回流到模板。
