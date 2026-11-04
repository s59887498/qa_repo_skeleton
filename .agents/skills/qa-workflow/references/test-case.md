# Mode: Test Case

輸入：來源版本、scope、已知規則/RBAC、期望格式。使用 generate-testcases 與 qa/methodology/test-design.md；已有案例先 review。
建立 requirement-condition-technique-evidence mapping；只有被確認的行為可寫 expected。缺 UI baseline、API contract 或 boundary 分別記 gap，不任意阻擋其他可設計範圍。
交付前使用 validate-testcases；記錄覆蓋口徑、未覆蓋理由、source gaps 與 review 狀態。不得把設計案例數當已測數。
