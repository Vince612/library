import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import sys

# Garante acesso ao módulo database na raiz
sys.path.append(r"c:\library")
import database

# =========================
# PAINEL USUÁRIO
# =========================
def painel_usuario():

    def carregar_livros():
        tabela_livros.delete(*tabela_livros.get_children())
        database.cursor.execute("""
            SELECT id, titulo, autor, quantidade_disponivel 
            FROM livros
        """)
        for row in database.cursor.fetchall():
            tabela_livros.insert("", tk.END, values=row)

    def carregar_bolsa():
        tabela_bolsa.delete(*tabela_bolsa.get_children())
        database.cursor.execute("""
            SELECT e.id, l.titulo, e.data_prevista_devolucao
            FROM emprestimos e
            JOIN livros l ON e.id_livro = l.id
            WHERE e.id_usuario=%s AND e.status='emprestado'
        """,(database.usuario_logado[0],))
        for row in database.cursor.fetchall():
            tabela_bolsa.insert("", tk.END, values=row)

    def carregar_historico():
        tabela_hist.delete(*tabela_hist.get_children())
        database.cursor.execute("""
            SELECT e.id, l.titulo, e.data_emprestimo,
                   e.data_devolucao, e.multa
            FROM emprestimos e
            JOIN livros l ON e.id_livro = l.id
            WHERE e.id_usuario=%s AND e.status='devolvido'
        """,(database.usuario_logado[0],))
        for row in database.cursor.fetchall():
            tabela_hist.insert("", tk.END, values=row)

    def emprestar():
        selecionado = tabela_livros.selection()
        if not selecionado:
            return

        item = tabela_livros.item(selecionado)
        livro_id = item['values'][0]
        disponivel = item['values'][3]

        if disponivel <= 0:
            messagebox.showerror("Erro", "Livro indisponível")
            return

        hoje = datetime.now().date()
        devolucao = hoje + timedelta(days=7)

        database.cursor.execute("""
            INSERT INTO emprestimos
            (id_usuario,id_livro,data_emprestimo,data_prevista_devolucao)
            VALUES (%s,%s,%s,%s)
        """,(database.usuario_logado[0],livro_id,hoje,devolucao))

        database.con.commit()
        carregar_livros()
        carregar_bolsa()
        messagebox.showinfo("Sucesso","Livro adicionado à sua bolsa 📚")

    def devolver():
        selecionado = tabela_bolsa.selection()
        if not selecionado:
            return

        item = tabela_bolsa.item(selecionado)
        emprestimo_id = item['values'][0]
        data_prevista = item['values'][2]

        hoje = datetime.now().date()

        if isinstance(data_prevista, str):
            data_prevista = datetime.strptime(data_prevista, "%Y-%m-%d").date()

        multa = 0
        if hoje > data_prevista:
            dias = (hoje - data_prevista).days
            multa = dias * 2

        database.cursor.execute("""
            UPDATE emprestimos
            SET data_devolucao=%s,
                multa=%s,
                status='devolvido'
            WHERE id=%s
        """,(hoje,multa,emprestimo_id))

        database.con.commit()
        carregar_bolsa()
        carregar_historico()

        if multa > 0:
            messagebox.showwarning("Multa aplicada",
                                   f"Atraso detectado.\nMulta: R${multa}")
        else:
            messagebox.showinfo("Devolvido","Livro devolvido com sucesso.")

    def pagar_multa():
        selecionado = tabela_hist.selection()
        if not selecionado:
            return

        item = tabela_hist.item(selecionado)
        emprestimo_id = item['values'][0]
        multa = item['values'][4]

        if multa == 0:
            messagebox.showinfo("Info","Não há multa para pagar.")
            return

        database.cursor.execute("""
            UPDATE emprestimos
            SET multa=0
            WHERE id=%s
        """,(emprestimo_id,))

        database.con.commit()
        carregar_historico()
        messagebox.showinfo("Pagamento","Multa paga com sucesso 💳")

    def limpar_historico():
        resposta = messagebox.askyesno("Confirmar",
                                       "Deseja limpar todo o histórico?")
        if resposta:
            database.cursor.execute("""
                DELETE FROM emprestimos
                WHERE id_usuario=%s AND status='devolvido'
            """,(database.usuario_logado[0],))
            database.con.commit()
            carregar_historico()

    def logout():
        janela.destroy()
        database.usuario_logado = None
        from login import tela_login
        tela_login()

    janela = tk.Tk()
    janela.title("Painel Usuário")
    janela.geometry("1000x650")

    tk.Label(janela,
             text=f"Bem-vindo {database.usuario_logado[1]}",
             font=("Arial",16,"bold")).pack(pady=10)

    tk.Button(janela, text="Sair", bg="#c0392b", fg="white", command=logout).pack(pady=5)

    notebook = ttk.Notebook(janela)
    notebook.pack(expand=True, fill="both")

    # ABA LIVROS
    aba_livros = tk.Frame(notebook)
    notebook.add(aba_livros, text="Livros")

    tabela_livros = ttk.Treeview(
        aba_livros,
        columns=("ID","Título","Autor","Disponível"),
        show="headings"
    )

    for col in tabela_livros["columns"]:
        tabela_livros.heading(col,text=col)

    tabela_livros.pack(pady=5)
    tk.Button(aba_livros,text="Emprestar",
              bg="#27ae60",fg="white",
              command=emprestar).pack(pady=5)
    tk.Button(aba_livros,text="Atualizar",
              bg="#2980b9",fg="white",
              command=carregar_livros).pack(pady=5)

    # ABA BOLSA
    aba_bolsa = tk.Frame(notebook)
    notebook.add(aba_bolsa, text="Minha Bolsa")

    tabela_bolsa = ttk.Treeview(
        aba_bolsa,
        columns=("ID","Livro","Devolução Prevista"),
        show="headings"
    )

    for col in tabela_bolsa["columns"]:
        tabela_bolsa.heading(col,text=col)

    tabela_bolsa.pack(pady=5)
    tk.Button(aba_bolsa,text="Devolver",
              bg="#c0392b",fg="white",
              command=devolver).pack(pady=5)

    # ABA HISTÓRICO
    aba_hist = tk.Frame(notebook)
    notebook.add(aba_hist, text="Histórico")

    tabela_hist = ttk.Treeview(
        aba_hist,
        columns=("ID","Livro","Emprestimo",
                 "Devolução","Multa"),
        show="headings"
    )

    for col in tabela_hist["columns"]:
        tabela_hist.heading(col,text=col)

    tabela_hist.pack(pady=5)

    tk.Button(aba_hist,text="Pagar Multa",
              bg="#f39c12",fg="white",
              command=pagar_multa).pack(pady=5)

    tk.Button(aba_hist,text="Limpar Histórico",
              bg="#7f8c8d",fg="white",
              command=limpar_historico).pack(pady=5)

    carregar_livros()
    carregar_bolsa()
    carregar_historico()

    janela.mainloop()