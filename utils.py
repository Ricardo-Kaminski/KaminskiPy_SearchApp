import PyPDF2
import docx
import webbrowser

# Função para abrir arquivos no visualizador padrão do sistema
def open_file(file_path):
    try:
        webbrowser.open_new(r'file://' + file_path)
    except Exception as e:
        raise ValueError(f"Erro ao abrir o arquivo {file_path}: {e}")



# Função para extrair texto de PDF
def extract_text_from_pdf(filepath):
    text = ""
    try:
        with open(filepath, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        raise ValueError(f"Erro ao extrair texto do PDF: {e}")
    return text

# Função para extrair texto de documentos DOCX
def extract_text_from_docx(filepath):
    text = ""
    try:
        doc = docx.Document(filepath)
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise ValueError(f"Erro ao extrair texto do DOCX: {e}")
    return text

# Função para carregar arquivos já processados
def load_processed_files():
    try:
        with open("processed_files.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Função para salvar arquivos processados
def save_processed_files(processed_files):
    with open("processed_files.json", "w") as f:
        json.dump(processed_files, f)
