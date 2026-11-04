# Readiness

每項輸入標 Ready、Missing、Not Required，列來源版本與 owner。Gate 是目前階段的判定，不是全產品品質背書。

| 階段 | 必要輸入 | 可先完成的工作 |
| --- | --- | --- |
| Plan / Cases | 需求範圍、來源、版本、預期交付 | source map、gap、design；憑證可稍後補 |
| Automation | Reviewed cases、contract、既有框架 | 缺 live access 可做本機測試與 mapping |
| Execution | steps、環境/build、access、資料、cleanup、evidence | 只跑已就緒 scope |
| Report | 實際結果、統計口徑、缺陷、限制 | evidence 不足時只做 Draft |

PASS：本階段輸入足夠；PARTIAL：部分可做，列受阻範圍；BLOCK：目前階段無法可靠完成。一次列重要缺漏，繼續不依賴缺漏的工作。
