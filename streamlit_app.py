from pathlib import Path
import io
import base64
import datetime
import streamlit as st

# ===== Paths =====
ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
LOGO = ASSETS / "logo.png"
FAVICON = ASSETS / "favicon.png"
CSS = ASSETS / "ui.css"

# ===== Branding =====
APP_NAME = "CMA Table Cleaner"
APP_TAGLINE = "Limpeza inteligente de DOCX/XLSX mantendo o layout"

# ===== Page config (primeiro) =====
st.set_page_config(
    page_title=f"{APP_NAME} • Crisley Matheus Automação",
    page_icon=str(FAVICON) if FAVICON.exists() else (str(LOGO) if LOGO.exists() else "🧹"),
    layout="centered"
)

# ===== CSS =====
if CSS.exists():
    st.markdown(f"<style>{CSS.read_text()}</style>", unsafe_allow_html=True)

# ===== Imports do app =====
from app.utils.filetype import get_ext
from app.services.excel import process_excel
from app.services.word import process_word

# ===== Header: LOGO sozinha + card do título separado =====
if LOGO.exists():
    logo_b64 = base64.b64encode(LOGO.read_bytes()).decode()
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; margin-top:20px; margin-bottom:12px;">
          <div class="logo-circle">
            <img src="data:image/png;base64,{logo_b64}" alt="Logo Crisley">
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    f"""
    <div class="brand">
      <h1>{APP_NAME}</h1>
      <div class="sub">{APP_TAGLINE}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ===== Card principal =====
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Arquivo (.xlsx ou .docx)",
        type=["xlsx", "docx"],
        help="Arraste e solte ou clique para selecionar. Suporte para Excel e Word."
    )
    names = st.text_input(
        "Nomes a excluir (separados por vírgula)",
        placeholder="Maria, João, Ana"
    )

    col_a, col_b = st.columns(2)
    with col_a:
        run = st.button("Processar", use_container_width=True)
    with col_b:
        clear = st.button("Limpar", use_container_width=True)

    if clear:
        st.rerun()

    if run:
        if not uploaded:
            st.error("Envie um arquivo .xlsx ou .docx.")
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

# ===== Footer centralizado com ano automático =====
year = datetime.datetime.now().year
st.markdown(
    f"""
    <div class="footer">
        © {year} Crisley Matheus Automação — simples, direto e funcional.
    </div>
    """,
    unsafe_allow_html=True
)
