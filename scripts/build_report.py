"""Create a run-scoped draft; never infer release approval from test success."""

import argparse
from collections import Counter
import json
from pathlib import Path

STATES = ("passed", "failed", "blocked", "skipped", "not_run")


def validate_results(data):
    if data.get("scope") != "run" or not isinstance(data.get("results"), list) or not data["results"]:
        raise ValueError("Non-empty run-scoped results are required")
    seen = set()
    for result in data["results"]:
        case_id = result.get("case_id")
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise ValueError("Results must have unique Case IDs; reconcile reruns explicitly")
        seen.add(case_id)
        if result.get("status") not in STATES or not result.get("actual") or not result.get("title"):
            raise ValueError("Each result needs status, actual, and title")
        evidence = result.get("evidence", [])
        if not isinstance(evidence, list) or any(not isinstance(item, str) or not item for item in evidence):
            raise ValueError("Evidence must be a list of non-empty references")
        if result["status"] in {"passed", "failed"} and not evidence:
            raise ValueError("Executed results require evidence")
    return Counter(result["status"] for result in data["results"])


def safe(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def build_report(data, evidence_source):
    counts = validate_results(data)
    lines = ["# 測試報告 — Run Draft", "", "## 1. 專案與版本", "",
             f"Environment：{safe(data.get('environment', '待確認'))}",
             f"Period：{safe(data.get('started_at', '未知'))} → {safe(data.get('finished_at', '未知'))}",
             "Build / owner：待依執行來源補齊。", "", "## 2. 已測範圍與限制", "",
             "僅涵蓋本次 run；不代表產品全量、正式環境或 Release 已通過。", "",
             "## 3. 結果統計", "", f"Unique cases：{len(data['results'])}",
             f"Runner exit code：{safe(data.get('exit_code', '未知'))}", "",
             "| Status | Count |", "| --- | ---: |"]
    lines.extend(f"| {state} | {counts[state]} |" for state in STATES)
    if ui := data.get("ui"):
        lines += ["", f"UI browser：{safe(ui['browser'])}",
                  f"Playwright artifacts directory：{safe(ui['output'])}",
                  f"Capture policy：trace={safe(ui['tracing'])}, screenshot={safe(ui['screenshot'])}",
                  "附件是否存在需依實際檔案確認；錄製政策不代表已產生附件。"]
    lines += ["", "| Case ID | Title | Status | Actual |", "| --- | --- | --- | --- |"]
    lines.extend("| " + " | ".join(safe(result[key]) for key in ("case_id", "title", "status", "actual")) + " |"
                 for result in data["results"])
    lines += ["", "## 4. 缺陷摘要", "", "Failed／Blocked 請依 evidence 收斂；本工具未建立外部 Bug。",
              "", "## 5. Evidence 與 Cleanup", "", f"Results source：{safe(evidence_source)}"]
    for result in data["results"]:
        lines.append(f"- {safe(result['case_id'])}：{safe(', '.join(result.get('evidence', [])) or '未執行')}")
    lines += ["", "Cleanup：待依 runner／人工紀錄核對。", "", "## 6. 風險與建議", "",
              "補列未測範圍、來源缺口、尚未排除缺陷。Runner 失敗或 evidence 不完整時不得直接升級為 Final。",
              "", "## 7. 交付與簽核", "", "Draft；未記錄正式交付或 Release approval。", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    data = json.loads(args.source.read_text(encoding="utf-8"))
    text = build_report(data, args.source.as_posix())
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(text, encoding="utf-8")
    print(f"Wrote run draft: {args.destination}")
