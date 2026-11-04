import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_readable_export_and_validator_agree(tmp_path):
    pytest.importorskip("openpyxl")
    export = script("export_cases")
    validator = script("validate_testcases")
    workbook = tmp_path / "Demo_Readable.xlsx"
    count = export.export_cases(ROOT / "qa/examples/catalog-cases.json", workbook)
    summary, issues = validator.validate_workbook(workbook)
    assert summary.cases == count == 10
    assert not issues


def test_validator_rejects_fractional_step_number(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    exporter = script("export_cases")
    validator = script("validate_testcases")
    path = tmp_path / "Broken_Readable.xlsx"
    exporter.export_cases(ROOT / "qa/examples/catalog-cases.json", path)
    workbook = openpyxl.load_workbook(path)
    workbook["Readable View"]["D3"] = 1.5
    workbook.save(path)
    summary, _ = validator.validate_workbook(path)
    assert summary.errors > 0


def test_formula_text_is_not_an_executable_excel_formula(tmp_path):
    openpyxl = pytest.importorskip("openpyxl")
    exporter = script("export_cases")
    data = json.loads((ROOT / "qa/examples/catalog-cases.json").read_text())
    data["cases"][0]["title"] = '=HYPERLINK("https://example.invalid", "demo")'
    source = tmp_path / "input.json"
    source.write_text(json.dumps(data))
    path = tmp_path / "Safe_Readable.xlsx"
    exporter.export_cases(source, path)
    assert openpyxl.load_workbook(path)["Case Index"]["B2"].data_type == "s"


@pytest.mark.parametrize("results", [
    [{"case_id": "CAT-001", "title": "Demo", "status": "passed", "actual": "ok", "evidence": []}],
    [{"case_id": "CAT-001", "title": "Demo", "status": "not_run", "actual": "pending"}] * 2,
    [],
])
def test_report_refuses_unsubstantiated_or_duplicate_results(results):
    with pytest.raises(ValueError):
        script("build_report").validate_results({"scope": "run", "results": results})


def test_report_preserves_unexecuted_scope_and_builds_word(tmp_path):
    docx = pytest.importorskip("docx")
    builder = script("build_report")
    data = {"scope": "run", "results": [
        {"case_id": "CAT-001", "title": "未執行示範", "status": "not_run", "actual": "待執行", "evidence": []}
    ]}
    markdown = builder.build_report(data, "synthetic-results.json")
    assert "| passed | 0 |" in markdown
    assert "| not_run | 1 |" in markdown
    source = tmp_path / "report.md"
    source.write_text(markdown)
    target = tmp_path / "report.docx"
    script("export_docx").export_docx(source, target)
    document = docx.Document(target)
    assert len([p for p in document.paragraphs if p.style.name == "Heading 1"]) == 7
    assert "CAT-001" in " ".join(c.text for table in document.tables for row in table.rows for c in row.cells)
