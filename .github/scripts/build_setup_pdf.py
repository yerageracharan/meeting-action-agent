from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak, KeepTogether
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "docs" / "Local-AI-and-API-Setup-Guide.md"
OUTPUT = ROOT / "docs" / "Local-AI-and-API-Setup-Guide.pdf"
PAGE_WIDTH, PAGE_HEIGHT = A4
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=27, leading=32, textColor=colors.HexColor("#19162a"), alignment=TA_LEFT, spaceAfter=12))
styles.add(ParagraphStyle(name="H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=20, leading=25, textColor=colors.HexColor("#3c2a60"), spaceBefore=14, spaceAfter=8))
styles.add(ParagraphStyle(name="H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#5a4588"), spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name="Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13, spaceAfter=5, textColor=colors.HexColor("#292738")))
styles.add(ParagraphStyle(name="Bulletx", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.1, leading=12, leftIndent=12, firstLineIndent=-8, spaceAfter=3))
styles.add(ParagraphStyle(name="Codex", parent=styles["Code"], fontName="Courier", fontSize=7.5, leading=10, leftIndent=9, rightIndent=9, borderColor=colors.HexColor("#d9d6e9"), borderWidth=.5, borderPadding=6, backColor=colors.HexColor("#f4f2fa"), spaceBefore=4, spaceAfter=8))
styles.add(ParagraphStyle(name="Smallx", parent=styles["BodyText"], fontName="Helvetica", fontSize=8, leading=11, textColor=colors.HexColor("#656174"), spaceAfter=5))

def inline_markup(text):
    text = escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<link href="\2" color="#5d4bb4">\1</link>', text)
    text = re.sub(r"(https?://[^\s]+)", r'<link href="\1" color="#5d4bb4">\1</link>', text)
    return text

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#ddd9e8"))
    canvas.line(18*mm, 15*mm, 192*mm, 15*mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6e6880"))
    canvas.drawString(18*mm, 9*mm, "Meeting Action Agent • Day 02 / 200")
    canvas.drawRightString(192*mm, 9*mm, f"Page {doc.page}")
    canvas.restoreState()

def build():
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    story = []
    i = 0
    first_heading = True
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip() or line.strip() == "---":
            story.append(Spacer(1, 3))
            i += 1
            continue
        img = re.match(r"!\[[^\]]*\]\(([^)]+)\)", line.strip())
        if img:
            image_path = (SOURCE.parent / img.group(1)).resolve()
            if image_path.exists() and image_path.suffix.lower() == ".svg":
                drawing = svg2rlg(str(image_path))
                if drawing:
                    max_w, max_h = 170*mm, 95*mm
                    scale = min(max_w / drawing.width, max_h / drawing.height, 1.0)
                    drawing.width *= scale
                    drawing.height *= scale
                    drawing.scale(scale, scale)
                    story.extend([Spacer(1, 4), drawing, Spacer(1, 6)])
            i += 1
            continue
        if line.startswith("# "):
            title = line[2:].strip()
            story.append(Paragraph(inline_markup(title), styles["CoverTitle"] if first_heading else styles["H1x"]))
            first_heading = False
            i += 1
            continue
        if line.startswith("## "):
            story.append(Paragraph(inline_markup(line[3:].strip()), styles["H1x"]))
            i += 1
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:].strip()), styles["H2x"]))
            i += 1
            continue
        if line.startswith("    ") or line.startswith("\t"):
            block = []
            while i < len(lines) and (lines[i].startswith("    ") or lines[i].startswith("\t")):
                block.append(lines[i][4:] if lines[i].startswith("    ") else lines[i][1:])
                i += 1
            story.append(Preformatted("\n".join(block), styles["Codex"]))
            continue
        if line.lstrip().startswith("|"):
            table_rows = []
            while i < len(lines) and lines[i].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c or "-") for c in cells):
                    table_rows.append("  •  ".join(cells))
                i += 1
            for row in table_rows:
                story.append(Paragraph(inline_markup(row), styles["Smallx"]))
            story.append(Spacer(1, 4))
            continue
        if line.startswith("- ") or re.match(r"^\d+\. ", line):
            bullet = "• " if line.startswith("- ") else ""
            text = line[2:] if line.startswith("- ") else re.sub(r"^\d+\. ", "", line)
            story.append(Paragraph(bullet + inline_markup(text), styles["Bulletx"]))
            i += 1
            continue
        if line.startswith("> "):
            story.append(Paragraph("<i>" + inline_markup(line[2:]) + "</i>", styles["Smallx"]))
            i += 1
            continue
        story.append(Paragraph(inline_markup(line), styles["Bodyx"]))
        i += 1
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=17*mm, bottomMargin=21*mm, title="Local AI and API Setup Guide")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Created {OUTPUT}")

if __name__ == "__main__":
    build()
