import tkinter as tk
from tkinter import ttk
import sys

# Garante acesso ao módulo database na raiz
sys.path.append(r"c:\library")
import database

# =========================
# PAINEL FUNCIONÁRIO
# =========================
def painel_funcionario():

    def atualizar_livros():
        tabela_livros.delete(*tabela_livros.get_children())
        database.cursor.execute("SELECT id,titulo,autor,quantidade_disponivel FROM livros")
        for row in database.cursor.fetchall():
            tabela_livros.insert("", tk.END, values=row)

    def atualizar_multas():
        tabela_multas.delete(*tabela_multas.get_children())
        database.cursor.execute("""
            SELECT u.nome, l.titulo, e.multa
            FROM emprestimos e
            JOIN usuarios u ON e.id_usuario = u.id
            JOIN livros l ON e.id_livro = l.id
            WHERE e.multa > 0 AND e.status = 'devolvido'
        """)
        for row in database.cursor.fetchall():
            tabela_multas.insert("", tk.END, values=row)

    def atualizar_devolvidos():
        tabela_devolvidos.delete(*tabela_devolvidos.get_children())
        database.cursor.execute("""
            SELECT u.nome, l.titulo, e.data_devolucao, e.multa
            FROM emprestimos e
            JOIN usuarios u ON e.id_usuario = u.id
            JOIN livros l ON e.id_livro = l.id
            WHERE e.status = 'devolvido'
            ORDER BY e.data_devolucao DESC
        """)
        for row in database.cursor.fetchall():
            tabela_devolvidos.insert("", tk.END, values=row)

    def adicionar():
        database.cursor.execute("""
            INSERT INTO livros (titulo,autor,quantidade_total,quantidade_disponivel)
            VALUES (%s,%s,%s,%s)
        """,(entry_titulo.get(),
             entry_autor.get(),
             entry_qtd.get(),
             entry_qtd.get()))
        database.con.commit()
        atualizar_livros()

    def remover():
        selecionado = tabela_livros.selection()
        if not selecionado:
            return
        item = tabela_livros.item(selecionado)
        livro_id = item['values'][0]

        database.cursor.execute("DELETE FROM livros WHERE id=%s",(livro_id,))
        database.con.commit()
        atualizar_livros()

    def editar():
        selecionado = tabela_livros.selection()
        if not selecionado:
            return
        item = tabela_livros.item(selecionado[0])
        livro_id = item['values'][0]

        database.cursor.execute("""
            UPDATE livros
            SET titulo=%s, autor=%s, quantidade_disponivel=%s
            WHERE id=%s
        """,(entry_titulo.get(),
             entry_autor.get(),
             entry_qtd.get(),
             livro_id))
        database.con.commit()
        atualizar_livros()

    def ao_selecionar(event):
        selecionado = tabela_livros.selection()
        if selecionado:
            item = tabela_livros.item(selecionado[0])
            valores = item['values']
            entry_titulo.delete(0, tk.END)
            entry_titulo.insert(0, valores[1])
            entry_autor.delete(0, tk.END)
            entry_autor.insert(0, valores[2])
            entry_qtd.delete(0, tk.END)
            entry_qtd.insert(0, valores[3])

    def logout():
        janela.destroy()
        database.usuario_logado = None
        from login import tela_login
        tela_login()

    janela = tk.Tk()
    janela.title("Painel Funcionário")
    janela.geometry("1000x700")

    tk.Button(janela, text="Sair", bg="#c0392b", fg="white", command=logout).pack(pady=5)

    notebook = ttk.Notebook(janela)
    notebook.pack(expand=True, fill="both")

    # =========================
    # ABA 1 - GERENCIAR LIVROS
    # =========================
    aba_livros = tk.Frame(notebook)
    notebook.add(aba_livros, text="Livros")

    tabela_livros = ttk.Treeview(
        aba_livros,
        columns=("ID","Título","Autor","Disponível"),
        show="headings"
    )

    for col in tabela_livros["columns"]:
        tabela_livros.heading(col,text=col)

    tabela_livros.pack(expand=True,fill="both",padx=20,pady=10)
    tabela_livros.bind("<<TreeviewSelect>>", ao_selecionar)

    frame = tk.Frame(aba_livros)
    frame.pack(pady=10)

    tk.Label(frame,text="Título").grid(row=0,column=0)
    entry_titulo = tk.Entry(frame)
    entry_titulo.grid(row=0,column=1)

    tk.Label(frame,text="Autor").grid(row=1,column=0)
    entry_autor = tk.Entry(frame)
    entry_autor.grid(row=1,column=1)

    tk.Label(frame,text="Quantidade").grid(row=2,column=0)
    entry_qtd = tk.Entry(frame)
    entry_qtd.grid(row=2,column=1)

    tk.Button(frame,text="Adicionar",
              bg="#2980b9",fg="white",
              command=adicionar).grid(row=3,column=0,pady=5)

    tk.Button(frame,text="Editar",
              bg="#f39c12",fg="white",
              command=editar).grid(row=3,column=1,pady=5)

    tk.Button(frame,text="Remover",
              bg="#c0392b",fg="white",
              command=remover).grid(row=3,column=2,pady=5)

    atualizar_livros()

    # =========================
    # ABA 2 - USUÁRIOS MULTADOS
    # =========================
    aba_multas = tk.Frame(notebook)
    notebook.add(aba_multas, text="Usuários Multados")

    tabela_multas = ttk.Treeview(
        aba_multas,
        columns=("Usuário","Livro","Multa"),
        show="headings"
    )

    for col in tabela_multas["columns"]:
        tabela_multas.heading(col,text=col)

    tabela_multas.pack(expand=True,fill="both",padx=20,pady=10)

    atualizar_multas()

    # =========================
    # ABA 3 - LIVROS DEVOLVIDOS
    # =========================
    aba_devolvidos = tk.Frame(notebook)
    notebook.add(aba_devolvidos, text="Livros Devolvidos")

    tabela_devolvidos = ttk.Treeview(
        aba_devolvidos,
        columns=("Usuário","Livro","Data Devolução","Multa"),
        show="headings"
    )

    for col in tabela_devolvidos["columns"]:
        tabela_devolvidos.heading(col,text=col)

    tabela_devolvidos.pack(expand=True,fill="both",padx=20,pady=10)

    atualizar_devolvidos()

    janela.mainloop()