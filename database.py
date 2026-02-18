import mysql.connector
from tkinter import messagebox
import sys

# =========================
# CONEXÃO MYSQL & ESTADO GLOBAL
# =========================
try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1999",
        database="library"
    )
    cursor = con.cursor()
except mysql.connector.Error as err:
    # Cria uma janela raiz temporária apenas para mostrar o erro, se o TK ainda não existir
    print(f"Erro de conexão: {err}")
    sys.exit(1)

usuario_logado = None