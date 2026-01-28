import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv
import pandas as pd

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

        

        return conn

    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

def fechar_conexao(conn):
    if conn:
        conn.close()
        


def DB_inserir_comercio(nome_fantasia, responsavel, cep, pais, estado, cidade, bairro, logradouro, numero):
    
    conn = conectar_banco()
    cursor = conn.cursor()

    comando_sql = """
    INSERT INTO comercios (nome_fantasia, responsavel, cep, pais, estado, cidade, bairro, logradouro, numero)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    valores = (nome_fantasia, responsavel, cep, pais, estado, cidade, bairro, logradouro, numero)
    cursor.execute(comando_sql, valores)
    conn.commit()
    print(f"Comercio {nome_fantasia} cadastrado com sucesso!")
        
    fechar_conexao(conn)

def DB_ler_comercios():

    conn = conectar_banco()
    cursor = conn.cursor()

    comando_sql = "SELECT * FROM comercios;"

    cursor.execute(comando_sql)
    resultados = cursor.fetchall()

    fechar_conexao(conn)
    
    return resultados

def DB_comercio_existe(nome_fantasia):

    conn = conectar_banco()
    cursor = conn.cursor()

    comando_sql = "SELECT EXISTS(SELECT 1 FROM comercios WHERE nome_fantasia = %s);"
    cursor.execute(comando_sql, (nome_fantasia,))
    resultado = cursor.fetchone()[0]

    fechar_conexao(conn)
    
    return resultado

def DB_obter_id_comercio(nome_fantasia):

    conn = conectar_banco()
    cursor = conn.cursor()

    comando_sql = "SELECT id_comercio FROM comercios WHERE nome_fantasia = %s;"
    cursor.execute(comando_sql, (nome_fantasia,))
    resultado = cursor.fetchone()

    fechar_conexao(conn)

    if resultado:
        return resultado[0]
    else:
        return None

def DB_buscar_ultimas_palavras_chave(nome_fantasia):
    conn = conectar_banco()
    cursor = conn.cursor()

    comando_sql = """
    SELECT
        sessoes.id_sessao
    FROM comercios
    INNER JOIN sessoes
    ON comercios.id_comercio = sessoes.id_comercio
    WHERE comercios.nome_fantasia = %s
    ORDER BY sessoes.data_pesquisa DESC 
    LIMIT 1;
    """
    cursor.execute(comando_sql, (nome_fantasia,))
    resultado = cursor.fetchone()

    if not resultado:
        fechar_conexao(conn)
        return [], None
    
    id_sessao = resultado[0]

    comando_sql = "SELECT termo_pesquisado FROM rank_palavras WHERE id_sessao = %s;"

    cursor.execute(comando_sql, (id_sessao,))
    resultados = [linha[0] for linha in cursor.fetchall()]

    fechar_conexao(conn)

    return resultados

def DB_inserir_resultados_busca(id_comercio, resultados):

    conn = conectar_banco()
    cursor = conn.cursor()

    comando_sql = "INSERT INTO sessoes (id_comercio) VALUES (%s) RETURNING id_sessao;"

    cursor.execute(comando_sql, (id_comercio,))
    id_sessao = cursor.fetchone()[0]

    dados_preparados = [(id_sessao, r[0], r[1], r[2]) for r in resultados]

    comando_sql = """
        INSERT INTO rank_palavras (id_sessao, termo_pesquisado, posicao, total_resultados)
        VALUES (%s, %s, %s, %s);"""

    cursor.executemany(comando_sql, dados_preparados)
    conn.commit()

    print("Resultados salvos com sucesso!")
    fechar_conexao(conn)

def procurar_rank_empresa_por_data(nome_comercio, data_inicio, data_fim):
    
    conn = conectar_banco()

    comando_sql = """
    SELECT
        rank_palavras.termo_pesquisado,
        rank_palavras.posicao,
        rank_palavras.total_resultados,
        sessoes.data_pesquisa
    FROM comercios
    INNER JOIN sessoes
    ON comercios.id_comercio = sessoes.id_comercio
    INNER JOIN rank_palavras
    ON sessoes.id_sessao = rank_palavras.id_sessao
    WHERE comercios.nome_fantasia = %s
    AND sessoes.data_pesquisa BETWEEN %s AND %s;
    """

    df = pd.read_sql(comando_sql, conn, params=(nome_comercio, data_inicio, data_fim))
    
    fechar_conexao(conn)

    return df