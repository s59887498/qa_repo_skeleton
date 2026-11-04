"""Export basic QA Markdown to Word. Render and review before formal delivery."""

import argparse
from pathlib import Path
import re


def export_docx(source, destination):
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Inches, Pt

    document = Document()
    normal = document.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Noto Sans CJK TC")
    section = document.sections[0]
    section.top_margin = section.bottom_margin = Inches(0.65)
    section.left_margin = section.right_margin = Inches(0.65)
    table = None
    for line in Path(source).read_text(encoding="utf-8").splitlines():
        if line.startswith("|"):
            if re.fullmatch(r"[| :\-]+", line):
                continue
            cells = [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", line)[1:-1]]
            if table is None:
                table = document.add_table(rows=1, cols=len(cells))
                table.style = "Light Shading Accent 1"
                row = table.rows[0]
                properties = row._tr.get_or_add_trPr()
                properties.append(OxmlElement("w:tblHeader"))
            else:
                row = table.add_row()
            if len(cells) != len(row.cells):
                raise ValueError("Inconsistent Markdown table width")
            for target, text in zip(row.cells, cells):
                target.text = text
            continue
        table = None
        if not line.strip():
            continue
        if line.startswith("# "):
            document.add_heading(line[2:], 0)
        elif line.startswith("## "):
            document.add_heading(line[3:], 1)
        elif line.startswith("### "):
            document.add_heading(line[4:], 2)
        elif line.startswith("- "):
            document.add_paragraph(line[2:], style="List Bullet")
        else:
            document.add_paragraph(line)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    document.save(destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    export_docx(args.source, args.destination)
    print(f"Exported {args.destination}; visual review is still required before delivery")
