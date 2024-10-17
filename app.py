import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Para o progresso
from search import search_index
from indexing import index_documents
from utils import open_file
import global_control  # Importar o controle global

# Variável para armazenar as pastas e contagem de arquivos
indexed_folders = {}

# Função para rodar a indexação em uma thread separada
def index_thread(root_folder, progress_label, progress_bar):
    global_control.stop_indexing = False  # Reinicia o estado da variável

    try:
        total_files = index_documents(root_folder, progress_label, progress_bar, indexed_folders)  # Passa o dicionário de pastas indexadas
        if not global_control.stop_indexing:
            progress_label.after(0, progress_label.config, {'text': "Indexação concluída com sucesso!"})
        else:
            progress_label.after(0, progress_label.config, {'text': "Indexação interrompida!"})
    except Exception as e:
        progress_label.after(0, progress_label.config, {'text': "Erro na indexação!"})
        messagebox.showerror("Erro", f"Erro ao indexar documentos: {e}")

    # Chamar a função de atualização da barra lateral após a indexação
    update_sidebar()

# Função para atualizar a barra lateral com pastas indexadas
def update_sidebar():
    folder_listbox.delete(0, tk.END)  # Limpar a lista antes de atualizar
    for folder, count in indexed_folders.items():
        folder_listbox.insert(tk.END, f"{folder} ({count} arquivos)")

# Função para abrir a janela de progresso
def show_progress_window(root_folder):
    progress_window = tk.Toplevel(root)  # Cria uma nova janela pop-up
    progress_window.title("Progresso da Indexação")
    progress_window.geometry("300x150")

    progress_label = tk.Label(progress_window, text="Iniciando indexação...")
    progress_label.pack(pady=10)

    # Barra de Progresso
    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=200, mode="determinate")
    progress_bar.pack(pady=10)
    progress_bar["value"] = 0  # Inicia com 0

    # Botão para parar a indexação
    stop_button = tk.Button(progress_window, text="Parar", command=stop_indexing_process)
    stop_button.pack(pady=10)

    # Iniciar a indexação em um novo thread
    thread = threading.Thread(target=index_thread, args=(root_folder, progress_label, progress_bar))
    thread.start()

def stop_indexing_process():
    global_control.stop_indexing = True  # Define como True para parar a indexação

# Atualizar a barra lateral após selecionar uma pasta
def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        indexed_folders[folder_selected] = 0  # Inicia a contagem de arquivos da pasta
        show_progress_window(folder_selected)  # Abre a janela de progresso
        update_sidebar()  # Atualiza a barra lateral imediatamente após a seleção da pasta

# Função para chamar a busca e atualizar a lista
def perform_search():
    term = search_entry.get()
    results = search_index(term)
    results_list.delete(0, tk.END)  # Limpa resultados anteriores
    if results:
        for result in results:
            results_list.insert(tk.END, result)
    else:
        results_list.insert(tk.END, "Nenhum resultado encontrado.")

# Função chamada ao clicar no resultado para abrir o arquivo
def on_result_click(event):
    selection = results_list.curselection()
    if selection:
        file_path = results_list.get(selection[0])
        open_file(file_path)

# Inicialização da interface gráfica (Tkinter)
root = tk.Tk()
root.title("Document Search App")

# Layout: Frame principal para conter a barra lateral e o conteúdo principal
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Barra lateral (Listbox) para exibir as pastas indexadas
sidebar_frame = tk.Frame(main_frame)
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

folder_listbox = tk.Listbox(sidebar_frame, width=40, height=20)
folder_listbox.pack(fill=tk.BOTH, expand=True)

# Área principal (Campo de busca e resultados)
content_frame = tk.Frame(main_frame)
content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Widgets da UI no frame de conteúdo
search_label = tk.Label(content_frame, text="Digite o termo de busca:")
search_label.pack()

search_entry = tk.Entry(content_frame, width=50)
search_entry.pack()

search_button = tk.Button(content_frame, text="Buscar", command=perform_search)
search_button.pack()

# Lista para mostrar os resultados
results_list = tk.Listbox(content_frame, width=80, height=20)
results_list.pack()

# Adicionar evento para clicar no item e abrir o arquivo
results_list.bind("<Double-1>", on_result_click)

# Botão para selecionar a pasta e indexar
index_button = tk.Button(content_frame, text="Selecionar Pasta para Indexar", command=select_folder)
index_button.pack()

# Iniciar a interface gráfica
root.mainloop()
