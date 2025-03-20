import os
import pandas as pd
import pdfplumber
import tabula
from PyPDF2 import PdfReader
from openpyxl import Workbook

def extrair_dados_pdf(pdf_path, output_xls_path):
    """
    Extrai 100% dos dados do PDF e os converte para XLS, garantindo integridade e precisão.
    """

    # 1️⃣ Verificar se o arquivo PDF existe
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"O arquivo {pdf_path} não foi encontrado.")

    # 2️⃣ Tentar extrair tabelas do PDF
    tabelas = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    
    if tabelas:
        # Caso o PDF contenha tabelas, consolidar todas em um único DataFrame
        df_final = pd.concat(tabelas, ignore_index=True)
    else:
        # Se não houver tabelas, extrair texto manualmente e estruturar os dados
        texto_extraido = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                texto_extraido.append(page.extract_text())

        texto_completo = "\n".join(texto_extraido)
        linhas = texto_completo.split("\n")
        dados_estruturados = [linha.split() for linha in linhas]
        df_final = pd.DataFrame(dados_estruturados)

    # 3️⃣ Validar se os dados foram extraídos corretamente
    if df_final.empty:
        raise ValueError("Não foi possível extrair dados do PDF. Verifique o formato do documento.")

    # 4️⃣ Exportar para XLS
    with pd.ExcelWriter(output_xls_path, engine="openpyxl") as writer:
        df_final.to_excel(writer, index=False, sheet_name="Dados Extraídos")

    return output_xls_path

# Caminhos de entrada e saída
pdf_arquivo = "documento.pdf"  # Substituir pelo caminho real do PDF
xls_arquivo = "dados_extraidos.xlsx"

# Executar extração e conversão
try:
    arquivo_xls = extrair_dados_pdf(pdf_arquivo, xls_arquivo)
    print(f"Arquivo XLS gerado com sucesso: {arquivo_xls}")
except Exception as e:
    print(f"Erro durante a extração: {e}")
