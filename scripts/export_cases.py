"""Build a readable workbook from reviewed, source-linked JSON cases."""

import argparse
import json
from pathlib import Path
import re


def load_cases(path):
    cases = json.loads(Path(path).read_text(encoding="utf-8"))["cases"]
    if not isinstance(cases, list) or not cases:
        raise ValueError("At least one reviewed case is required")
    seen = set()
    for case in cases:
        for field in ("id", "title", "module", "priority", "source", "preconditions", "cleanup"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                raise ValueError(f"Non-empty {field} is required")
        if not re.fullmatch(r"[A-Z][A-Z0-9_]{1,20}-\d{3,6}", case["id"]) or case["id"] in seen:
            raise ValueError("Case IDs must be unique uppercase IDs with a numeric suffix")
        seen.add(case["id"])
        if case["priority"] not in {"High", "Medium", "Low"}:
            raise ValueError("Invalid priority")
        if case.get("state", "Not Started") != "Not Started":
            raise ValueError("Design export initializes Not Started; execution evidence must be recorded separately")
        if not isinstance(case.get("tags"), list) or any(not isinstance(tag, str) for tag in case["tags"]):
            raise ValueError("tags must be a list of strings")
        if not case.get("steps") or any(not step.get("action") or not step.get("expected") for step in case["steps"]):
            raise ValueError("Every step needs action and expected")
    return cases


def export_cases(source, destination):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    cases = load_cases(source)
    workbook = Workbook()
    readme = workbook.active
    readme.title = "README_使用說明"
    readme.append(["Readable Test Cases"])
    readme.append(["Case Index 是範圍索引；Readable View 是執行與 Review 主表。"])
    readme.append(["所有案例初始 Not Started；格式驗證不代表已 Review 或已執行。"])
    readme.append(["前置條件與 cleanup 在每個 step row 保留；來源是 JSON 的 source 欄位。"])
    readme.column_dimensions["A"].width = 105
    index = workbook.create_sheet("Case Index")
    index.append(["Test Case ID", "Title", "Module", "Priority", "Step Count", "State", "Tags", "Source", "Notes"])
    readable = workbook.create_sheet("Readable View")
    readable.append(["逐步執行；每一列均有預期結果。此檔是設計交付，沒有實測結果。"])
    readable.append(["Test Case ID", "Title", "Preconditions", "Step #", "Steps", "Expected Result", "Cleanup", "Source"])
    for case in cases:
        index.append([case["id"], case["title"], case["module"], case["priority"], len(case["steps"]),
                      "Not Started", ",".join(case["tags"]), case["source"], case.get("notes", "")])
        for step_number, step in enumerate(case["steps"], 1):
            readable.append([case["id"], case["title"], case["preconditions"], step_number,
                             step["action"], step["expected"], case["cleanup"], case["source"]])
    for sheet, header_row, widths in [
        (index, 1, [18, 34, 18, 14, 14, 18, 32, 50, 42]),
        (readable, 2, [18, 32, 42, 10, 52, 52, 42, 50]),
    ]:
        sheet.freeze_panes = f"C{header_row + 1}"
        sheet.auto_filter.ref = f"A{header_row}:{get_column_letter(sheet.max_column)}{sheet.max_row}"
        for column, width in enumerate(widths, 1):
            sheet.column_dimensions[get_column_letter(column)].width = width
        for row in sheet.iter_rows():
            for cell in row:
                cell.alignment = Alignment(vertical="top", wrap_text=True)
                # Untrusted source text must never become an Excel formula.
                if isinstance(cell.value, str):
                    cell.data_type = "s"
                if cell.row == header_row:
                    cell.fill = PatternFill("solid", fgColor="17365D")
                    cell.font = Font(color="FFFFFF", bold=True)
                elif cell.row > header_row and cell.row % 2:
                    cell.fill = PatternFill("solid", fgColor="EEF3F8")
            sheet.row_dimensions[row[0].row].height = 65 if row[0].row > header_row else 30
        sheet.sheet_properties.pageSetUpPr.fitToPage = True
        sheet.page_setup.orientation = "landscape"
        sheet.page_setup.paperSize = sheet.PAPERSIZE_A3
        sheet.page_setup.fitToWidth = 1
        sheet.page_setup.fitToHeight = 0
        sheet.print_title_rows = f"{header_row}:{header_row}"
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(destination)
    return len(cases)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(f"Exported {export_cases(args.source, args.destination)} designed cases to {args.destination}")
