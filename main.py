from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors

from datetime import datetime
import calendar

year = datetime.now().year
file_path = f"./calendario-{year}.pdf"

pagesize = landscape(A4)

doc = SimpleDocTemplate(
    file_path,
    pagesize=pagesize,
    rightMargin=20,
    leftMargin=20,
    topMargin=20,
    bottomMargin=20
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="MonthTitle",
    fontSize=36,
    alignment=1,
    spaceAfter=6
))

elements = []

calendar.setfirstweekday(calendar.MONDAY)

months_es = [
    "Enero","Febrero","Marzo","Abril","Mayo","Junio",
    "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
]

days_es = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

page_width, page_height = pagesize
usable_width = page_width - doc.leftMargin - doc.rightMargin
usable_height = page_height - doc.topMargin - doc.bottomMargin

col_width = usable_width / 7
row_height = (usable_height - 80) / 7  # header + 6 semanas

for month in range(1, 13):
    elements.append(Paragraph(f"{months_es[month-1]}", styles["MonthTitle"]))
    elements.append(Spacer(1, 50))

    cal = calendar.monthcalendar(year, month)
    table_data = [days_es]

    for week in cal:
        table_data.append([str(d) if d != 0 else "" for d in week])

    table = Table(
        table_data,
        colWidths=[col_width]*7,
        rowHeights=[row_height]*len(table_data)
    )

    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1.5, colors.black),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONT", (0,0), (-1,0), "Helvetica-Bold"),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("FONTSIZE", (0,0), (-1,0), 18),
        ("FONTSIZE", (0,1), (-1,-1), 26),
        ("TOPPADDING", (0,0), (-1,-1), 22),
        ("BOTTOMPADDING", (0,0), (-1,-1), 22),
    ]))

    elements.append(table)

    if month != 12:
        elements.append(PageBreak())

doc.build(elements)
