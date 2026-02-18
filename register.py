import tkinter as tk
from tkinter import messagebox
import sys

# Garante acesso ao módulo database na raiz
sys.path.append(r"c:\library")
import database

def tela_cadastro():
    # Importação tardia para evitar erro de importação circular com login.py
    from login import tela_login

    def salvar():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()

        if not nome or not email or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return

        try:
            database.cursor.execute("""
                INSERT INTO usuarios (nome, email, senha, tipo)
                VALUES (%s, %s, %s, 'usuario')
            """, (nome, email, senha))
            database.con.commit()
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            janela.destroy()
            tela_login()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar conta: {e}")

    def voltar():
        janela.destroy()
        tela_login()

    janela = tk.Tk()
    janela.title("Criar Conta")
    janela.geometry("300x350")

    tk.Label(janela, text="Nome").pack(pady=5)
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Email").pack(pady=5)
    entry_email = tk.Entry(janela)
    entry_email.pack()

    tk.Label(janela, text="Senha").pack(pady=5)
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.pack()

    tk.Button(janela, text="Cadastrar", bg="#27ae60", fg="white", command=salvar).pack(pady=20)
    tk.Button(janela, text="Voltar", command=voltar).pack()

    janela.mainloop()