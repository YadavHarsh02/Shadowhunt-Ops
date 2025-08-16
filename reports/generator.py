# reports/generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_simple_report(filepath: str, title: str, rows: list[dict]):
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, title)
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Generated: {datetime.utcnow().isoformat()}Z")
    y -= 20
    for r in rows:
        line = f"[{r.get('timestamp','')}] {r.get('module','')} → {r.get('target','')} :: {r.get('output','')}"
        for chunk in _wrap(line, 95):
            y -= 14
            if y < 50:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)
            c.drawString(40, y, chunk)
    c.showPage()
    c.save()

def _wrap(text, width):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 <= width:
            line = (line + " " + w).strip()
        else:
            out.append(line); line = w
    if line: out.append(line)
    return out
