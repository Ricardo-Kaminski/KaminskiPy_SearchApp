import json
import os
import PyPDF2
import docx
import webbrowser

# Abrir arquivos no leitor padrão
def open_file(file_path):
    webbrowser.open(file_path)

# Função para extrair texto de PDF
def extract_text_from_pdf(filepath):
    text = ""
    with open(filepath, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
    return text

# Função para extrair texto de DOCX
def extract_text_from_docx(filepath):
    doc = docx.Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])

# Função para carregar arquivos já processados
def load_processed_files():
    if os.path.exists("processed_files.json"):
        with open("processed_files.json", "r") as f:
            return json.load(f)
    return {}

# Função para salvar arquivos processados
def save_processed_files(processed_files):
    with open("processed_files.json", "w") as f:
        json.dump(processed_files, f)
