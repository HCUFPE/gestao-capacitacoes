from typing import List, Dict, Any
import pandas as pd
import io

async def export_to_excel(data: List[Dict[str, Any]], filename: str = "export.xlsx") -> io.BytesIO:
    """
    Exporta uma lista de dicionários para um arquivo Excel em memória.

    Args:
        data: Lista de dicionários a serem exportados.
        filename: Nome do arquivo (usado para metadados, não para salvar no disco).

    Returns:
        Um objeto BytesIO contendo o arquivo Excel.
    """
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    output.seek(0)
    return output
