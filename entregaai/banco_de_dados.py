import psycopg2
import pandas as pd

# Função para conectar ao banco de dados PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",  # Nome do banco de dados
            user="postgres",    # Usuário
            password="Humilde123!",  # Senha
            host="localhost",   # Host (localhost para local, ou IP/URL do servidor)
            port="5432"         # Porta padrão do PostgreSQL
        )
        return conn
    except psycopg2.OperationalError as e:
        print("Erro ao conectar ao banco de dados:", e)
        raise

# Função para executar uma consulta SQL e retornar resultados
def execute_query(query, params=None):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            result = cur.fetchall()
            return result
    except Exception as e:
        print("Erro ao executar a consulta:", e)
    finally:
        conn.close()

    
def update_status(query):
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            print(f"Status updated for product_name: {query}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Fechar a conexão
        conn.close()
