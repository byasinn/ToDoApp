import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

# Caminho do arquivo JSON para salvar as tarefas
FILE_PATH = "tasks.json"

# Funções para carregar e salvar tarefas
def load_tasks():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(FILE_PATH, "w") as file:
        json.dump(tasks, file)

# Classe do Aplicativo de Lista de Tarefas
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tarefas Moderno")
        self.root.geometry("500x600")
        self.root.config(bg="#f0f4f8")

        # Carregar tarefas
        self.tasks = load_tasks()
        
        # Configuração da interface
        self.setup_ui()

    def setup_ui(self):
        # Barra lateral para o título
        sidebar = tk.Frame(self.root, width=200, bg="#324a5f")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        title = tk.Label(sidebar, text="Tarefas", font=("Helvetica", 18, "bold"), bg="#324a5f", fg="#ffffff")
        title.pack(pady=20)

        # Área principal
        main_area = tk.Frame(self.root, bg="#f0f4f8")
        main_area.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Entrada de nova tarefa
        self.task_entry = tk.Entry(main_area, font=("Helvetica", 14), bg="#ffffff", fg="#000000", relief="flat", bd=2)
        self.task_entry.pack(fill=tk.X, padx=10, pady=10)

        # Menu de seleção de categoria
        self.category_var = tk.StringVar(value="Geral")
        category_menu = ttk.Combobox(main_area, textvariable=self.category_var, values=["Geral", "Trabalho", "Estudo", "Pessoal"])
        category_menu.pack(fill=tk.X, padx=10, pady=5)

        # Botão de adicionar tarefa
        add_button = tk.Button(main_area, text="Adicionar Tarefa", command=self.add_task, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), relief="flat")
        add_button.pack(fill=tk.X, padx=10, pady=5)

        # Filtro de categoria
        filter_frame = tk.Frame(main_area, bg="#f0f4f8")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(filter_frame, text="Filtrar por Categoria:", bg="#f0f4f8", font=("Helvetica", 12)).pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="Todas")
        filter_menu = ttk.Combobox(filter_frame, textvariable=self.filter_var, values=["Todas", "Geral", "Trabalho", "Estudo", "Pessoal"])
        filter_menu.pack(side=tk.LEFT, padx=5)
        filter_menu.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())

        # Listbox para exibir tarefas
        self.tasks_listbox = tk.Listbox(main_area, width=50, height=15, selectmode=tk.SINGLE, font=("Helvetica", 12), bg="#ffffff", fg="#324a5f", bd=0, highlightthickness=0)
        self.tasks_listbox.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
        
        # Botões de ações para as tarefas
        button_frame = tk.Frame(main_area, bg="#f0f4f8")
        button_frame.pack(pady=10)

        complete_button = tk.Button(button_frame, text="Concluir", command=self.complete_task, bg="#2196F3", fg="white", font=("Helvetica", 10, "bold"), relief="flat")
        complete_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Excluir", command=self.delete_task, bg="#e53935", fg="white", font=("Helvetica", 10, "bold"), relief="flat")
        delete_button.pack(side=tk.LEFT, padx=5)

        # Carregar as tarefas existentes
        self.load_tasks_into_listbox()

    # Função para adicionar uma nova tarefa
    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text:
            task = {"text": task_text, "category": self.category_var.get(), "completed": False}
            self.tasks.append(task)
            self.task_entry.delete(0, tk.END)
            self.save_and_reload()
        else:
            messagebox.showwarning("Aviso", "Por favor, insira uma tarefa.")

    # Função para marcar uma tarefa como concluída
    def complete_task(self):
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            self.tasks[selected_index]["completed"] = not self.tasks[selected_index]["completed"]
            self.save_and_reload()
        except IndexError:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione uma tarefa para marcar como concluída.")

    # Função para excluir uma tarefa
    def delete_task(self):
        try:
            selected_index = self.tasks_listbox.curselection()[0]
            del self.tasks[selected_index]
            self.save_and_reload()
        except IndexError:
            messagebox.showwarning("Seleção Inválida", "Por favor, selecione uma tarefa para excluir.")

    # Função para salvar e atualizar a lista
    def save_and_reload(self):
        save_tasks(self.tasks)
        self.load_tasks_into_listbox()

    # Função para carregar as tarefas na listbox com estilo para tarefas concluídas
    def load_tasks_into_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_text = task["text"] + (" [Concluída]" if task["completed"] else "")
            self.tasks_listbox.insert(tk.END, task_text)
            
            # Aplicar estilo para tarefas concluídas
            if task["completed"]:
                self.tasks_listbox.itemconfig(tk.END, {'fg': 'grey', 'selectbackground': '#d3d3d3'})

    # Função para aplicar filtro por categoria
    def apply_filter(self):
        selected_category = self.filter_var.get()
        self.tasks_listbox.delete(0, tk.END)
        
        for task in self.tasks:
            if selected_category == "Todas" or task["category"] == selected_category:
                task_text = task["text"] + (" [Concluída]" if task["completed"] else "")
                self.tasks_listbox.insert(tk.END, task_text)
                
                # Aplicar estilo para tarefas concluídas
                if task["completed"]:
                    self.tasks_listbox.itemconfig(tk.END, {'fg': 'grey', 'selectbackground': '#d3d3d3'})

# Inicializar o aplicativo
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
