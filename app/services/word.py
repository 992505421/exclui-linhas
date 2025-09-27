from typing import List, Tuple
from docx import Document
import io
import re

def process_word(content: bytes, original_name: str, names: List[str]) -> Tuple[bytes, str]:
    doc = Document(io.BytesIO(content))
    r = re.compile("|".join(map(re.escape, names)), re.IGNORECASE)

    for table in doc.tables:
        rows_to_remove = []
        for row in table.rows:
            row_text = " | ".join(cell.text or "" for cell in row.cells)
            if r.search(row_text):
                rows_to_remove.append(row)
        for row in rows_to_remove:
            tbl = row._tr.getparent()
            tbl.remove(row._tr)

    out = io.BytesIO()
    doc.save(out)
    out.seek(0)
    new_name = f"{original_name.rsplit('.',1)[0]}_limpo.docx"
    return out.read(), new_name
