from typing import List, Tuple
from fastapi import HTTPException

def process_pdf(content: bytes, original_name: str, names: List[str]) -> Tuple[bytes, str]:
    # Ainda não suportado (remoção "perfeita" de linhas em PDF exige reconstrução de layout)
    raise HTTPException(status_code=501, detail="PDF ainda não suportado para remoção de linhas mantendo layout.")
