import io
import streamlit as st
from app.utils.filetype import get_ext
from app.services.excel import process_excel
from app.services.word import process_word
from app.services.pdf import process_pdf  # v1: 501

st.set_page_config(page_title="Exclui Linhas", page_icon="🧹", layout="centered")
st.title("🧹 Excluir linhas por nome (DOCX/XLSX)")

st.markdown("Arraste o arquivo e informe os nomes (separados por vírgula).")
uploaded = st.file_uploader("Arquivo (.xlsx, .docx ou .pdf)", type=["xlsx", "docx", "pdf"])
names = st.text_input("Nomes a excluir (separados por vírgula)", placeholder="João, Maria, Ana")

run = st.button("Processar")

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
                st.warning("PDF ainda não suportado para remover linhas mantendo layout. (v2) ")
                out_bytes, out_name = process_pdf(content, uploaded.name, names_list)  # vai lançar 501
                mime = "application/pdf"
            else:
                st.error("Formato não suportado.")
                st.stop()

            st.success("Processado com sucesso.")
            st.download_button(
                label=f"Baixar {out_name}",
                data=io.BytesIO(out_bytes),
                file_name=out_name,
                mime=mime,
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Erro ao processar: {e}")
