import os
import tkinter as tk
from tkinter import filedialog, messagebox
from search import search_index
from indexing import index_documents
from utils import open_file

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

# Função para selecionar pasta e indexar
def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        try:
            index_documents(folder_selected)
            messagebox.showinfo("Sucesso", f"Documentos indexados da pasta: {folder_selected}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao indexar documentos: {e}")

# Função chamada ao clicar no resultado para abrir o arquivo
def on_result_click(event):
    selection = results_list.curselection()
    if selection:
        file_path = results_list.get(selection[0])
        open_file(file_path)

# Inicialização da interface gráfica (Tkinter)
root = tk.Tk()
root.title("Document Search App")

# Widgets da UI
search_label = tk.Label(root, text="Digite o termo de busca:")
search_label.pack()

search_entry = tk.Entry(root, width=50)
search_entry.pack()

search_button = tk.Button(root, text="Buscar", command=perform_search)
search_button.pack()

# Lista para mostrar os resultados
results_list = tk.Listbox(root, width=80, height=20)
results_list.pack()

# Adicionar evento para clicar no item e abrir o arquivo
results_list.bind("<Double-1>", on_result_click)

# Botão para selecionar a pasta e indexar
index_button = tk.Button(root, text="Selecionar Pasta para Indexar", command=select_folder)
index_button.pack()

# Iniciar a interface gráfica
root.mainloop()
