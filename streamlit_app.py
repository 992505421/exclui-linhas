import io
from pathlib import Path
import streamlit as st

from app.utils.filetype import get_ext
from app.services.excel import process_excel
from app.services.word import process_word
from app.services.pdf import process_pdf  # continua 501

# ---- Page config (usa logo como ícone se quiser) ----
LOGO_PATH = Path("logo.png")  # coloque seu logo aqui
st.set_page_config(
    page_title="Excluir Linhas • Crisley Matheus Informática",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "🧹",
    layout="centered"
)

# ---- Carregar CSS ----
css_path = Path("app/ui.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# ---- Header bonito ----
col_logo, col_text = st.columns([0.18, 0.82], vertical_alignment="center")
with col_logo:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), use_container_width=True)
with col_text:
    st.markdown("""
    <div class="brand-hero">
      <div>
        <h1>Excluir linhas por nome</h1>
        <div class="subtitle">DOCX • XLSX  —  Layout preservado • Paleta oficial</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ---- Card principal ----
st.markdown('<div class="card">', unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Arquivo (.xlsx, .docx ou .pdf)",
    type=["xlsx", "docx", "pdf"],
    help="Arraste e solte ou clique para selecionar. Limite sugerido: 200 MB."
)
names = st.text_input("Nomes a excluir (separados por vírgula)", placeholder="Maria, João, Ana")

colA, colB = st.columns(2)
with colA:
    run = st.button("Processar", use_container_width=True)
with colB:
    clear = st.button("Limpar", use_container_width=True)

if clear:
    st.rerun()

if run:
    if not uploaded:
        st.error("Envie um arquivo.")
    elif not names.strip():
        st.error("Informe ao menos um nome.")
    else:
        ext = get_ext(uploaded.name)
        names_list = [n.strip() for n in names.split(",") if n.strip()]
        content = uploaded.read()

        try:
            if ext == "xlsx":
                out_bytes, out_name = process_excel(content, uploaded.name, names_list)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif ext == "docx":
                out_bytes, out_name = process_word(content, uploaded.name, names_list)
                mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            elif ext == "pdf":
                st.markdown('<div class="notice">PDF ainda não suportado mantendo layout. (v2 em desenvolvimento)</div>', unsafe_allow_html=True)
                out_bytes, out_name = process_pdf(content, uploaded.name, names_list)  # 501
                mime = "application/pdf"
            else:
                st.error("Formato não suportado.")
                st.stop()

            st.success("Pronto! Baixe o arquivo limpo:")
            st.download_button(
                f"⬇️ Baixar {out_name}",
                data=io.BytesIO(out_bytes),
                file_name=out_name,
                mime=mime,
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Erro: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# ---- Rodapé curtinho (opcional)
st.caption("© Crisley Matheus Informática — Automação que simplifica.")
