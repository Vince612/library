import tkinter as tk
from tkinter import messagebox
import sys

# Garante acesso ao módulo database na raiz
sys.path.append(r"c:\library")
import database
from user import painel_usuario
from admin import painel_funcionario
from register import tela_cadastro

# =========================
# LOGIN
# =========================

def tela_login():

    def entrar():
        email = entry_email.get()
        senha = entry_senha.get()
        modo_funcionario = var_funcionario.get()

        database.cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        user = database.cursor.fetchone()

        if not user:
            messagebox.showerror("Erro", "Usuário não encontrado")
            return

        if user[3] != senha:
            messagebox.showerror("Erro", "Senha incorreta")
            return

        # Se marcou modo funcionário mas não é funcionário
        if modo_funcionario and user[4] not in ['funcionario','admin']:
            messagebox.showerror("Erro", "Você não é funcionário")
            return

        database.usuario_logado = user
        login.destroy()

        if user[4] in ['funcionario','admin']:
            painel_funcionario()
        else:
            painel_usuario()

    def abrir_cadastro():
        login.destroy()
        tela_cadastro()

    login = tk.Tk()
    login.title("Biblioteca - Login")
    login.geometry("350x300")
    login.config(bg="#2c3e50")

    tk.Label(login, text="LOGIN",
             font=("Arial",18,"bold"),
             bg="#2c3e50", fg="white").pack(pady=20)

    tk.Label(login, text="Email",
             bg="#2c3e50", fg="white").pack()
    entry_email = tk.Entry(login, width=30)
    entry_email.pack(pady=5)

    tk.Label(login, text="Senha",
             bg="#2c3e50", fg="white").pack()
    entry_senha = tk.Entry(login, show="*", width=30)
    entry_senha.pack(pady=5)

    var_funcionario = tk.BooleanVar()
    tk.Checkbutton(login,
                   text="Entrar como Funcionário",
                   variable=var_funcionario,
                   bg="#2c3e50",
                   fg="white",
                   selectcolor="#2c3e50").pack(pady=5)

    tk.Button(login, text="Entrar",
              bg="#27ae60", fg="white",
              width=20, command=entrar).pack(pady=10)

    tk.Button(login, text="Criar Conta",
              bg="#2980b9", fg="white",
              width=20,
              command=abrir_cadastro).pack()

    login.mainloop()