# src/helpers/pdf_helper.py
from typing import List, Dict, Any
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

async def export_to_pdf(data: List[Dict[str, Any]], filename: str = "report.pdf") -> BytesIO:
    """
    Exports a list of dictionaries to a PDF file in memory.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    story = []
    story.append(Paragraph("Relatório de Cursos por Lotação", styles['h1']))
    story.append(Paragraph("<br/><br/>", styles['Normal']))

    if not data:
        story.append(Paragraph("Nenhum dado para exibir.", styles['Normal']))
    else:
        # Extract headers
        headers = list(data[0].keys())
        table_data = [headers] + [[str(item[header]) for header in headers] for item in data]

        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer