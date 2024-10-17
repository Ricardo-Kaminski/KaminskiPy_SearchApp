import os
import json
import logging
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from utils import extract_text_from_pdf, extract_text_from_docx, load_processed_files, save_processed_files
import global_control  # Importar o controle global

# Definir o esquema globalmente
schema = Schema(title=TEXT(stored=True), path=TEXT(stored=True), content=TEXT)

# Configuração de logging para registrar os erros
logging.basicConfig(filename='index_errors.log', level=logging.ERROR)

# Função para indexar os documentos
def index_documents(root_folder, progress_label, progress_bar, indexed_folders):
    processed_files = load_processed_files()
    
    # Criar o diretório de índices, se não existir
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    
    # Criar ou abrir o índice
    ix = create_in("indexdir", schema) if not os.path.exists("indexdir") else open_dir("indexdir")
    writer = ix.writer()

    total_files = 0
    for root, dirs, files in os.walk(root_folder):
        total_files += len(files)

    file_count = 0  # Contador de arquivos processados

    # Configurar a barra de progresso
    progress_bar["maximum"] = total_files

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if global_control.stop_indexing:  # Verifica se a indexação deve parar
                writer.commit()  # Salva o índice atual antes de parar
                return

            file_path = os.path.join(root, file)

            # Ignorar arquivos temporários
            if file.startswith('~$'):
                continue

            try:
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

                        # Atualizar o progresso
                        file_count += 1
                        indexed_folders[root_folder] = file_count  # Atualiza a contagem de arquivos da pasta
                        progress_percentage = (file_count / total_files) * 100
                        
                        # Atualizar a barra de progresso
                        progress_bar["value"] = file_count

                        progress_label.after(0, progress_label.config, {'text': f"Indexando... {file_count}/{total_files} arquivos ({progress_percentage:.2f}% concluído)"})

                    except Exception as e:
                        logging.error(f"Erro ao indexar {file_path}: {e}")
                        continue  # Pula para o próximo arquivo sem interromper o processo

            except OSError as e:
                logging.error(f"Erro ao acessar {file_path}: {e}")
                continue  # Pula para o próximo arquivo

    # Finalizar a escrita no índice
    writer.commit()
    
    # Salvar a lista de arquivos processados
    save_processed_files(processed_files)

