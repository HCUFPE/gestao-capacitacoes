from typing import List, Dict, Any
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

async def export_to_pdf(data: List[Dict[str, Any]], filename: str = "export.pdf") -> io.BytesIO:
    """
    Exporta uma lista de dicionários para um arquivo PDF em memória.

    Args:
        data: Lista de dicionários a serem exportados.
        filename: Nome do arquivo (usado para metadados, não para salvar no disco).

    Returns:
        Um objeto BytesIO contendo o arquivo PDF.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f"Relatório de Dados - {filename}", styles['h1']))
    story.append(Spacer(1, 0.2 * letter[1]))

    if data:
        # Prepare table data
        headers = list(data[0].keys())
        table_data = [headers]
        for row in data:
            table_data.append([str(row.get(header, '')) for header in headers])

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
    else:
        story.append(Paragraph("Nenhum dado para exportar.", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer
