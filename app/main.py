from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.process import router as process_router

app = FastAPI(title="Exclui Linhas - DOCX/XLSX", version="1.0.0", docs_url="/", redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(process_router, prefix="/api")
