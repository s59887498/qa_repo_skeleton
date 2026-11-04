#!/usr/bin/env python3
"""Validate Readable Test Case workbooks against the repo QA standard."""

from __future__ import annotations

import argparse
import glob
import json
import posixpath
import re
import sys
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"main": MAIN_NS, "rel": REL_NS, "pkg": PACKAGE_REL_NS}

REQUIRED_SHEETS = ("README_使用說明", "Case Index", "Readable View")
INDEX_REQUIRED = ("Test Case ID", "Title", "Module", "Priority", "Step Count", "State")
READABLE_REQUIRED = ("Test Case ID", "Step #", "Steps", "Expected Result")
ID_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]{1,20}-\d{3,6}$")
ALLOWED_PRIORITIES = {"High", "Medium", "Low"}
ALLOWED_STATES = {"Not Started", "Blocked", "Passed", "Failed", "Skipped"}


@dataclass
class Issue:
    severity: str
    path: str
    sheet: str | None
    row: int | None
    field: str | None
    message: str


@dataclass
class FileSummary:
    path: str
    cases: int = 0
    steps: int = 0
    errors: int = 0
    warnings: int = 0


def add_issue(
    issues: list[Issue],
    severity: str,
    path: Path,
    message: str,
    sheet: str | None = None,
    row: int | None = None,
    field: str | None = None,
) -> None:
    issues.append(Issue(severity, str(path), sheet, row, field, message))


def column_index(address: str) -> int:
    letters = "".join(character for character in address if character.isalpha())
    result = 0
    for character in letters:
        result = result * 26 + ord(character.upper()) - ord("A") + 1
    return result


def cell_text(cell: ET.Element, shared_strings: list[str]) -> str:
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        return "".join(cell.itertext()).strip()

    value = cell.find("main:v", NS)
    if value is None or value.text is None:
        return ""
    if cell_type == "s":
        try:
            return shared_strings[int(value.text)]
        except (IndexError, ValueError):
            return ""
    return value.text.strip()


def read_shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(item.itertext()) for item in root.findall("main:si", NS)]


def sheet_paths(archive: zipfile.ZipFile) -> dict[str, str]:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {
        relationship.get("Id"): relationship.get("Target", "")
        for relationship in rels.findall("pkg:Relationship", NS)
    }
    result: dict[str, str] = {}
    for sheet in workbook.findall("main:sheets/main:sheet", NS):
        relationship_id = sheet.get(f"{{{REL_NS}}}id")
        target = targets.get(relationship_id, "")
        if sheet.get("name") and target:
            target = target.lstrip("/")
            result[sheet.get("name")] = posixpath.normpath(target if target.startswith("xl/") else posixpath.join("xl", target))
    return result


def read_sheet(archive: zipfile.ZipFile, path: str, shared_strings: list[str]) -> dict[int, dict[int, str]]:
    root = ET.fromstring(archive.read(path))
    rows: dict[int, dict[int, str]] = {}
    for row in root.findall("main:sheetData/main:row", NS):
        row_number = int(row.get("r", "0"))
        values: dict[int, str] = {}
        for cell in row.findall("main:c", NS):
            address = cell.get("r", "")
            if address:
                values[column_index(address)] = cell_text(cell, shared_strings)
        if row_number:
            rows[row_number] = values
    return rows


def header_map(row: dict[int, str]) -> dict[str, int]:
    return {value.strip(): column for column, value in row.items() if value.strip()}


def expand_paths(inputs: list[str]) -> list[Path]:
    if not inputs:
        inputs = ["qa/outputs/testcases/**/*_Readable.xlsx"]

    paths: list[Path] = []
    for item in inputs:
        matches = [Path(match) for match in glob.glob(item, recursive=True)]
        if matches:
            for match in matches:
                paths.extend(sorted(match.rglob("*.xlsx")) if match.is_dir() else [match])
            continue
        candidate = Path(item)
        paths.extend(sorted(candidate.rglob("*.xlsx")) if candidate.is_dir() else [candidate])

    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(path)
    return unique


def require_headers(
    path: Path,
    sheet: str,
    headers: dict[str, int],
    expected: tuple[str, ...],
    issues: list[Issue],
) -> bool:
    missing = [header for header in expected if header not in headers]
    if missing:
        add_issue(issues, "ERROR", path, f"Missing required header(s): {', '.join(missing)}.", sheet, 1)
    return not missing


def value(row: dict[int, str], headers: dict[str, int], name: str) -> str:
    return row.get(headers.get(name, -1), "").strip()


def whole_number(text: str) -> int:
    if not re.fullmatch(r"[0-9]+(?:\.0+)?", text):
        raise ValueError("Expected a whole number")
    return int(text.split(".")[0])


def validate_workbook(path: Path) -> tuple[FileSummary, list[Issue]]:
    summary = FileSummary(str(path))
    issues: list[Issue] = []

    if not path.exists():
        add_issue(issues, "ERROR", path, "File does not exist.")
        summary.errors = 1
        return summary, issues
    if path.suffix.lower() != ".xlsx":
        add_issue(issues, "ERROR", path, "Expected an .xlsx Readable Test Case workbook.")
        summary.errors = 1
        return summary, issues

    try:
        with zipfile.ZipFile(path) as archive:
            shared_strings = read_shared_strings(archive)
            paths = sheet_paths(archive)
            missing_sheets = [sheet for sheet in REQUIRED_SHEETS if sheet not in paths]
            if missing_sheets:
                add_issue(issues, "ERROR", path, f"Missing required worksheet(s): {', '.join(missing_sheets)}.")
                summary.errors = 1
                return summary, issues
            index_rows = read_sheet(archive, paths["Case Index"], shared_strings)
            readable_rows = read_sheet(archive, paths["Readable View"], shared_strings)
    except (ET.ParseError, KeyError, OSError, zipfile.BadZipFile) as error:
        add_issue(issues, "ERROR", path, f"Unable to read workbook: {error}.")
        summary.errors = 1
        return summary, issues

    index_headers = header_map(index_rows.get(1, {}))
    readable_headers = header_map(readable_rows.get(2, {}))
    index_ready = require_headers(path, "Case Index", index_headers, INDEX_REQUIRED, issues)
    readable_ready = require_headers(path, "Readable View", readable_headers, READABLE_REQUIRED, issues)
    if not index_ready or not readable_ready:
        summary.errors = len([issue for issue in issues if issue.severity == "ERROR"])
        return summary, issues

    index_cases: dict[str, tuple[int, dict[int, str]]] = {}
    for row_number in sorted(number for number in index_rows if number >= 2):
        row = index_rows[row_number]
        case_id = value(row, index_headers, "Test Case ID")
        if not case_id:
            continue
        if case_id in index_cases:
            add_issue(issues, "ERROR", path, "Duplicate Test Case ID.", "Case Index", row_number, "Test Case ID")
            continue
        index_cases[case_id] = (row_number, row)
        summary.cases += 1
        for field in ("Title", "Module", "Priority", "State"):
            if not value(row, index_headers, field):
                add_issue(issues, "ERROR", path, "Required field is blank.", "Case Index", row_number, field)
        if not ID_PATTERN.match(case_id):
            add_issue(issues, "WARN", path, "Test Case ID should use an uppercase prefix and numeric suffix, such as GEN-0001.", "Case Index", row_number, "Test Case ID")
        priority = value(row, index_headers, "Priority")
        if priority and priority not in ALLOWED_PRIORITIES:
            add_issue(issues, "WARN", path, f"Unexpected Priority '{priority}'.", "Case Index", row_number, "Priority")
        state = value(row, index_headers, "State")
        if state and state not in ALLOWED_STATES:
            add_issue(issues, "WARN", path, f"Unexpected State '{state}'.", "Case Index", row_number, "State")
        tags = value(row, index_headers, "Tags")
        if "，" in tags:
            add_issue(issues, "ERROR", path, "Tags must use English commas, not full-width commas.", "Case Index", row_number, "Tags")

    steps_by_case: dict[str, list[tuple[int, int]]] = {}
    for row_number in sorted(number for number in readable_rows if number >= 3):
        row = readable_rows[row_number]
        case_id = value(row, readable_headers, "Test Case ID")
        if not case_id:
            continue
        step_text = value(row, readable_headers, "Steps")
        expected = value(row, readable_headers, "Expected Result")
        step_number_text = value(row, readable_headers, "Step #")
        if not step_text:
            add_issue(issues, "ERROR", path, "Steps must not be blank.", "Readable View", row_number, "Steps")
        if not expected:
            add_issue(issues, "ERROR", path, "Expected Result must not be blank.", "Readable View", row_number, "Expected Result")
        try:
            step_number = whole_number(step_number_text)
        except ValueError:
            add_issue(issues, "ERROR", path, "Step # must be a positive integer.", "Readable View", row_number, "Step #")
            continue
        if step_number < 1:
            add_issue(issues, "ERROR", path, "Step # must be a positive integer.", "Readable View", row_number, "Step #")
            continue
        steps_by_case.setdefault(case_id, []).append((row_number, step_number))
        summary.steps += 1

    for case_id, rows in steps_by_case.items():
        actual_numbers = [step_number for _, step_number in rows]
        expected_numbers = list(range(1, len(rows) + 1))
        if actual_numbers != expected_numbers:
            add_issue(issues, "ERROR", path, f"Step # must be sequential from 1; found {actual_numbers}.", "Readable View", rows[0][0], "Step #")
        if case_id not in index_cases:
            add_issue(issues, "ERROR", path, "Test Case ID is missing from Case Index.", "Readable View", rows[0][0], "Test Case ID")

    for case_id, (row_number, row) in index_cases.items():
        steps = steps_by_case.get(case_id, [])
        if not steps:
            add_issue(issues, "ERROR", path, "Test Case ID has no step rows in Readable View.", "Case Index", row_number, "Test Case ID")
            continue
        step_count = value(row, index_headers, "Step Count")
        if not step_count:
            add_issue(issues, "ERROR", path, "Step Count is required.", "Case Index", row_number, "Step Count")
        if step_count:
            try:
                if whole_number(step_count) != len(steps):
                    add_issue(issues, "ERROR", path, f"Step Count is {step_count}, but Readable View has {len(steps)} step row(s).", "Case Index", row_number, "Step Count")
            except ValueError:
                add_issue(issues, "ERROR", path, "Step Count must be a whole number.", "Case Index", row_number, "Step Count")

    if not index_cases:
        add_issue(issues, "ERROR", path, "No cases in Case Index.")
    summary.errors = len([issue for issue in issues if issue.severity == "ERROR"])
    summary.warnings = len([issue for issue in issues if issue.severity == "WARN"])
    return summary, issues


def print_human(summaries: Iterable[FileSummary], issues: list[Issue]) -> None:
    summaries = list(summaries)
    print(f"Validated {len(summaries)} workbook(s), {sum(item.cases for item in summaries)} test case(s), {sum(item.steps for item in summaries)} step(s).")
    print(f"Errors: {sum(item.errors for item in summaries)}  Warnings: {sum(item.warnings for item in summaries)}")
    for issue in issues:
        location = issue.path
        if issue.sheet:
            location += f":{issue.sheet}"
        if issue.row is not None:
            location += f":{issue.row}"
        field = f" [{issue.field}]" if issue.field else ""
        print(f"{issue.severity}: {location}{field} {issue.message}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Readable .xlsx files, directories, or glob patterns. Defaults to qa/outputs/testcases/**/*_Readable.xlsx.")
    parser.add_argument("--warnings-as-errors", action="store_true", help="Return failure when warnings exist.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable text.")
    args = parser.parse_args(argv)

    summaries: list[FileSummary] = []
    issues: list[Issue] = []
    for path in expand_paths(args.paths):
        summary, file_issues = validate_workbook(path)
        summaries.append(summary)
        issues.extend(file_issues)

    if args.json:
        print(json.dumps({"files": [asdict(item) for item in summaries], "issues": [asdict(item) for item in issues]}, ensure_ascii=False, indent=2))
    else:
        print_human(summaries, issues)

    if not summaries:
        print("No workbooks matched; validation did not run.", file=sys.stderr)
        return 1
    errors = sum(item.errors for item in summaries)
    warnings = sum(item.warnings for item in summaries)
    return 1 if errors or (args.warnings_as_errors and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
