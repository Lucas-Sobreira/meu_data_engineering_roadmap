from pathlib import Path
import os

import pandas as pd 
import pandera as pa
from dotenv import load_dotenv
from sqlalchemy import create_engine

# from schema import ProdutoSchema, ProductSchemaKPI

def load_settings(): 
    """
    Carrega as configurações a partir de variáveis de ambiente.
    """
    dotenv_path = Path.cwd() / '.env'
    load_dotenv(dotenv_path = dotenv_path)

    settings = {
        "db_host": os.getenv("POSTGRES_HOST"),
        "db_user": os.getenv("POSTGRES_USER"),
        "db_pass": os.getenv("POSTGRES_PASSWORD"),
        "db_name": os.getenv("POSTGRES_DB"),
        "db_port": os.getenv("POSTGRES_PORT"),
    }
    return settings

def extrair_do_sql(query: str) -> pd.DataFrame:
    """
    Extrai dados do banco de dados SQL usando a consulta fornecida.

    Args:
        query: A consulta SQL para extrair dados.

    Returns:
        Um DataFrame do Pandas contendo os dados extraídos.
    """
    settings = load_settings()

    # Criar a string de conexão com base nas configurações
    connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"

    # Criar engine de conexão
    engine = create_engine(connection_string)

    with engine.connect() as conn, conn.begin():
            df_crm = pd.read_sql(query, conn)

    return df_crm

if __name__ == "__main__": 
     query = "SELECT * FROM produtos_bronze_email"
     df_crm = extrair_do_sql(query=query)
     schema_crm = pa.infer_schema(df_crm)

     with open('./app/schema_crm.json', 'w', encoding='utf-8') as arquivo: 
          arquivo.write(schema_crm.to_script())

     print(df_crm)