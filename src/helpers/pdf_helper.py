# src/helpers/pdf_helper.py
from typing import List, Dict, Any
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Mapeamento de chaves de dados para rótulos legíveis em português
COLUMN_LABELS = {
    "nome_profissional": "Nome",
    "cpf": "CPF",
    "vinculo": "Vínculo",
    "setor": "Setor",
    "nome_curso": "Curso",
    "plataforma": "Plataforma",
    "carga_horaria": "CH",
    "ano_gd": "Ano GD",
    "certificado": "Certificado",
    "status": "Status",
    "data_envio_certificado": "Data Envio",
    "certificado_enviado": "Cert. Enviado",
}

# Larguras relativas por prioridade: colunas de texto longo recebem mais espaço
COLUMN_WEIGHTS = {
    "nome_profissional": 20,
    "nome_curso": 20,
    "vinculo": 10,
    "setor": 10,
    "plataforma": 10,
    "cpf": 12,
    "carga_horaria": 5,
    "ano_gd": 5,
    "certificado": 8,
    "status": 8,
    "data_envio_certificado": 10,
    "certificado_enviado": 8,
    # Default para chaves não mapeadas
}
DEFAULT_WEIGHT = 10


def _get_column_headers(keys: List[str]) -> List[str]:
    """Retorna rótulos legíveis para cada chave de coluna."""
    return [COLUMN_LABELS.get(k, k.replace("_", " ").title()) for k in keys]


def _calculate_col_widths(headers: List[str], page_width: float, margins: float) -> List[float]:
    """Calcula larguras de coluna proporcionais baseadas nos pesos."""
    available_width = page_width - margins
    weights = [COLUMN_WEIGHTS.get(h, DEFAULT_WEIGHT) for h in headers]
    total_weight = sum(weights)
    return [(w / total_weight) * available_width for w in weights]


def _cell_value(item: Dict[str, Any], key: str) -> str:
    """Converte valor de célula para string segura."""
    val = item.get(key)
    if val is None:
        return "—"
    if isinstance(val, bool):
        return "Sim" if val else "Não"
    return str(val)


async def export_to_pdf(data: List[Dict[str, Any]], filename: str = "report.pdf") -> BytesIO:
    """
    Exports a list of dictionaries to a PDF file in memory.
    
    Layout:
    - Página Letter (8.5 x 11 polegadas = 612 x 792 pts)
    - Margens de 0.5 inch (36 pts) em cada lado
    - Larguras de coluna calculadas proporcionalmente
    - Word wrap automático via Paragraph
    - Quebra de página a cada ~25 linhas para evitar cortes
    - Cabeçalhos repetidos em cada página via TableStyle
    """
    buffer = BytesIO()
    page_width, page_height = letter  # 612 x 792
    left_margin = right_margin = 0.5 * inch  # 36 pts
    top_margin = bottom_margin = 0.75 * inch  # 54 pts
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=left_margin,
        rightMargin=right_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
    )
    styles = getSampleStyleSheet()
    
    story = []
    story.append(Paragraph("Relatório de Cursos por Lotação", styles["h1"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    if not data:
        story.append(Paragraph("Nenhum dado para exibir.", styles["Normal"]))
    else:
        keys = list(data[0].keys())
        headers = _get_column_headers(keys)
        col_widths = _calculate_col_widths(headers, page_width, left_margin + right_margin)

        # Cabeçalho da tabela
        header_row = [Paragraph(h, styles["Heading4"]) for h in headers]
        
        # Construir linhas de dados usando Paragraph para word wrap
        data_rows = []
        for item in data:
            row = []
            for key in keys:
                text = _cell_value(item, key)
                # Centralizar colunas numéricas/curtas
                alignment = TA_CENTER if key in ("carga_horaria", "ano_gd", "certificado", "certificado_enviado", "status") else TA_LEFT
                row.append(Paragraph(text, styles["Normal"]))
                # Guardar alinhamento para aplicar no estilo
            data_rows.append(row)

        # Dividir em chunks para evitar páginas muito longas
        # ~25 linhas por tabela permite quebra natural de página
        rows_per_page = 25
        all_table_data = [header_row] + data_rows
        
        style_commands = [
            # Cabeçalho
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3B5998")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            # Dados
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("TOPPADDING", (0, 1), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            # Alinhamento por tipo de coluna
        ]

        # Adicionar alinhamento específico por coluna
        for i, key in enumerate(keys):
            if key in ("carga_horaria", "ano_gd", "certificado", "certificado_enviado", "status"):
                style_commands.append(("ALIGN", (i, 1), (i, -1), "CENTER"))
            else:
                style_commands.append(("ALIGN", (i, 1), (i, -1), "LEFT"))
        
        # Zebra striping
        for row_idx in range(1, len(all_table_data)):
            if row_idx % 2 == 0:
                style_commands.append(("BACKGROUND", (0, row_idx), (-1, row_idx), colors.HexColor("#F8F9FA")))

        # Se poucos dados, tabela única
        if len(data_rows) <= rows_per_page:
            table = Table(all_table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(TableStyle(style_commands))
            story.append(table)
        else:
            # Dividir em múltiplas tabelas com quebra de página
            for start in range(0, len(data_rows), rows_per_page):
                chunk = data_rows[start:start + rows_per_page]
                table_data = [header_row] + chunk
                table = Table(table_data, colWidths=col_widths, repeatRows=1)
                table.setStyle(TableStyle(style_commands))
                
                if start > 0:
                    story.append(PageBreak())
                story.append(table)

    doc.build(story)
    buffer.seek(0)
    return buffer
