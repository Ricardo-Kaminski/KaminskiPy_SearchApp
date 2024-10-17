import os
import json
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from utils import extract_text_from_pdf, extract_text_from_docx, load_processed_files, save_processed_files

# Definir o esquema globalmente
schema = Schema(title=TEXT(stored=True), path=TEXT(stored=True), content=TEXT)

def index_documents(root_folder):
    processed_files = load_processed_files()
    
    # Criar o diretório de índices, se não existir
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    
    # Criar ou abrir o índice
    ix = create_in("indexdir", schema) if not os.path.exists("indexdir") else open_dir("indexdir")
    writer = ix.writer()

    # Percorrer as pastas e subpastas
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            last_modified = os.path.getmtime(file_path)

            # Verificar se o arquivo já foi indexado
            if file_path not in processed_files or processed_files[file_path] != last_modified:
                try:
                    # Indexar arquivos PDF
                    if file.lower().endswith(".pdf"):
                        text = extract_text_from_pdf(file_path)
                        writer.add_document(title=file, path=file_path, content=text)
                    
                    # Indexar arquivos DOCX
                    elif file.lower().endswith(".docx"):
                        text = extract_text_from_docx(file_path)
                        writer.add_document(title=file, path=file_path, content=text)

                    # Atualizar os arquivos processados
                    processed_files[file_path] = last_modified

                except Exception as e:
                    print(f"Erro ao indexar {file_path}: {e}")

    # Finalizar a escrita no índice
    writer.commit()
    
    # Salvar a lista de arquivos processados
    save_processed_files(processed_files)
