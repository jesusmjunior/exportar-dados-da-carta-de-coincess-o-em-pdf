import streamlit as st
import pandas as pd
import pdfplumber
import tempfile
import io

st.set_page_config(page_title="Extrator PDF → Excel", layout="centered")

st.title("📄 Extrator de Dados PDF para Excel")

st.write("Envie um arquivo PDF e receba um Excel com os dados extraídos.")

# Função para extrair texto do PDF
def extrair_texto_pdf(pdf_file):
    texto_extraido = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            texto_extraido.append(page.extract_text())
    return "\n".join(texto_extraido)

# Função para estruturar texto em DataFrame
def estruturar_texto(texto):
    linhas = texto.split("\n")
    dados = [linha.split() for linha in linhas if linha]
    df = pd.DataFrame(dados)
    return df

# Upload do PDF
uploaded_pdf = st.file_uploader("Envie o PDF", type=['pdf'])

if uploaded_pdf:
    try:
        # Extração
        st.info("🔍 Extraindo dados do PDF...")
        texto_pdf = extrair_texto_pdf(uploaded_pdf)

        df = estruturar_texto(texto_pdf)

        if df.empty:
            st.warning("⚠️ Não foi possível extrair dados estruturados do PDF.")
        else:
            st.success("✅ Dados extraídos com sucesso!")
            st.dataframe(df)

            # Download do arquivo Excel sem salvar localmente
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Dados Extraídos')
            buffer.seek(0)

            st.download_button(
                label="📥 Baixar Excel (XLSX)",
                data=buffer,
                file_name="dados_extraidos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Erro ao processar o PDF: {e}")
