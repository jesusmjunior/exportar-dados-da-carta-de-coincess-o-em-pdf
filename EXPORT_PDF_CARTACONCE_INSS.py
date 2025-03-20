import streamlit as st
import pandas as pd
import pdfplumber
import tempfile

st.set_page_config(page_title="Extrator de PDF para Excel", layout="centered")

st.title("📄🔁 Extrator de Dados PDF → Excel (XLSX)")

st.write("Faça upload do PDF contendo tabelas ou texto estruturado e converta para planilha XLSX.")

# ⬆️ Upload do PDF
uploaded_pdf = st.file_uploader("Envie o arquivo PDF", type=['pdf'])

if uploaded_pdf:
    try:
        # Criação de arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(uploaded_pdf.read())
            pdf_path = tmp_pdf.name

        st.success("✅ PDF carregado com sucesso!")

        # 🟡 Função para extrair dados com pdfplumber
        def extrair_texto_pdf(pdf_path):
            texto_extraido = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    texto_extraido.append(page.extract_text())
            return "\n".join(texto_extraido)

        # 🟡 Estruturar dados extraídos
        def estruturar_texto(texto):
            linhas = texto.split("\n")
            dados = [linha.split() for linha in linhas if linha]
            return pd.DataFrame(dados)

        # Extração
        texto_pdf = extrair_texto_pdf(pdf_path)
        df = estruturar_texto(texto_pdf)

        if df.empty:
            st.error("❌ Não foi possível extrair dados estruturados deste PDF.")
        else:
            st.dataframe(df)

            # Download do Excel
            output = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            df.to_excel(output.name, index=False)

            with open(output.name, 'rb') as f:
                st.download_button(
                    "📥 Baixar Excel (XLSX)",
                    data=f,
                    file_name="dados_extraidos.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"❌ Erro durante a extração: {e}")
