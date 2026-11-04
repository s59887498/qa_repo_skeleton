# 測試設計方法

先建立可追溯的設計 Map：`Requirement → Condition → Technique → Coverage item → Evidence lane → Automation decision → Setup/Data/Cleanup → Source/Gap`。

| 技法 | 適用條件 | 輸入不足時 | 常見覆蓋單位 |
| --- | --- | --- | --- |
| Equivalence Partitioning (`Technique_EP`) | 可區分等價輸入群組 | 不自行編造類別預期 | valid / invalid partition |
| Boundary Value Analysis (`Technique_BVA`) | 有明確範圍、精度及包含規則 | 不猜 min/max；記缺口 | 邊界與相鄰跨界值 |
| Decision Table (`Technique_DT`) | 多條件決定動作 | 未知規則留待確認 | 可行 rule column |
| State Transition (`Technique_ST`) | 已知狀態、事件、guard | 不推測 enum / transition | 合法與禁止轉移 |
| Use Case (`Technique_UC`) | 有使用者目標與流程 | 只做有來源的主要／替代流程 | end-to-end path |

技法標籤只標實際採用的技法；API／UI 是 evidence lane，不是技法。風險探索與假設先進 backlog，只有確認且可追溯的項目才轉正式 Expected Result。
缺憑證不阻擋案例設計。缺 UI baseline 不可宣稱 visual PASS；DOM geometry、screenshot、accessibility、API response 分別留證。
優先自動化穩定回歸、高風險且可觀測的流程；目前不適合者寫 blocker、owner、解除條件，不能無期限標 Manual only。
