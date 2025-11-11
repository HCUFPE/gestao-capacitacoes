# src/helpers/excel_helper.py
from typing import List, Dict, Any
from io import BytesIO
import pandas as pd

async def export_to_excel(data: List[Dict[str, Any]]) -> BytesIO:
    """
    Exports a list of dictionaries to an Excel file in memory.
    """
    df = pd.DataFrame(data)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Relatorio')
    writer.close() # Use close() instead of save() for newer pandas versions
    output.seek(0)
    return output