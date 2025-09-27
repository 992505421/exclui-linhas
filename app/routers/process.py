import io
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from app.utils.filetype import get_ext
from app.services.excel import process_excel
from app.services.word import process_word
from app.services.pdf import process_pdf

router = APIRouter(tags=["process"])

@router.post("/process")
async def process_file(
    file: UploadFile = File(..., description="Arquivo .xlsx, .docx ou .pdf"),
    names: str = Form(..., description="Lista separada por vírgula")
):
    ext = get_ext(file.filename)
    if ext not in {"xlsx", "docx", "pdf"}:
        raise HTTPException(status_code=400, detail="Formato não suportado. Use .xlsx, .docx ou .pdf")

    names_list: List[str] = [n.strip() for n in names.split(",") if n.strip()]
    if not names_list:
        raise HTTPException(status_code=400, detail="Informe pelo menos um nome.")

    raw = await file.read()

    if ext == "xlsx":
        out_bytes, out_name = process_excel(raw, file.filename, names_list)
        media = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif ext == "docx":
        out_bytes, out_name = process_word(raw, file.filename, names_list)
        media = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    else:  # pdf
        out_bytes, out_name = process_pdf(raw, file.filename, names_list)
        media = "application/pdf"

    return StreamingResponse(
        io.BytesIO(out_bytes),
        media_type=media,
        headers={"Content-Disposition": f'attachment; filename="{out_name}"'}
    )
