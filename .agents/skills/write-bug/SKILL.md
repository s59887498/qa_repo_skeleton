---
name: write-bug
description: "將可重現問題或 failed case 收斂為簡潔 Bug Draft；已授權且 destination 明確時才建立 tracker issue。"
---

# Write Bug

先讀 `qa/templates/bug.md` 與 project profile 的 tracker routing。沒有 destination/parent 或授權時保存 `qa/outputs/bugs/<project>/<feature>/` Draft。
一單一個可獨立修正的原因。標題描述使用者看得到的錯誤；包含環境/build、最小步驟、actual、expected/source、影響、短 evidence 與 Case ID。
預期行為無來源時列需求待確認；不把推測當確認缺陷。去除敏感資訊、冗長 payload、重複敘述。
使用已連接 tracker 的原生工具；開單前核對 project/parent 和既有重複單。不繼承來源公司的固定 project ID/section。
建立、留言、重派、關閉分別遵守使用者已授權範圍；建立 Bug 不等於授權通知其他人或關閉單。
