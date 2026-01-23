import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv()

def conectar_banco():
    try:
        
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            port=os.getenv("DB_PORT")
        )

        print("Conexão com o banco de dados estabelecida com sucesso.")

        return conn

    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

def fechar_conexao(conn):
    if conn:
        conn.close()
        print("Conexão com o banco de dados fechada.")

conn = conectar_banco()
fechar_conexao(conn)