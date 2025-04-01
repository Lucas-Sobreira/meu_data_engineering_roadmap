import os
from dotenv import load_dotenv
from datetime import datetime
from loguru import logger

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import boto3

# ===================== CONFIGURAÇÃO DE LOGS =====================
datetime_now = datetime.now().strftime("%Y-%m-%d")
log_dir = os.path.join(os.getcwd(), "files/logs/s3_parquet/")    
os.makedirs(log_dir, exist_ok=True) # Garante que a pasta exista
log_path= os.path.join(log_dir, f'app{datetime_now}.log')
logger.add(log_path, format="{time} {level} {message}", level="INFO")


# ===================== FUNÇÕES ==============================
def verifica_arquivos_source() -> bool:
    """ 
    Verifica se há arquivos na pasta 'source'.
    Se a pasta estiver vazia, encerra o DAG sem erro.
    """
    source_path = os.path.join(os.getcwd(), "files/data/source/")
    arquivos = os.listdir(source_path)

    if arquivos:
        print(f"📂 Arquivos encontrados na pasta Source: {arquivos}")
        logger.info(f"📂 Arquivos encontrados na pasta Source: {arquivos}")
        return True  # Permite que o fluxo continue
    else:
        print("⚠️ Nenhum arquivo encontrado na pasta Source. Encerrando DAG.")
        logger.info("⚠️ Nenhum arquivo encontrado na pasta Source. Encerrando DAG.")
        return False  # O Airflow entenderá que não há trabalho a ser feito e tentará novamente na próxima execução.

def load_settings() -> dict: 
    dotenv_path = os.path.join(os.getcwd(), "files/.env")
    load_dotenv(dotenv_path=dotenv_path)
    settings = {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region_name": os.getenv("REGION_NAME"),
        "bucket_name": os.getenv("BUCKET_NAME")
    }
    return settings

def configurando_ambiente() -> list:
    print("Configurando os diretórios dos arquivos")
    source_dir = os.path.join(os.getcwd(), "files/data/source/")
    output_dir = os.path.join(os.getcwd(), "files/data/output_files/")
    path_list = [source_dir, output_dir]
    print(f"path_list: {path_list}")
    logger.info(f"Caminho das pastas configurados com sucesso!\n{path_list}")
    return path_list

def arquivos_output(path_list: list) -> None:
    source_dir = path_list[0]
    output_dir = path_list[1]
    extensions = ["json", "parquet"]

    for file_extension in extensions:
        try: 
            name= os.path.join(output_dir, f"{file_extension}/")
            logger.info(f"Pasta para os arquivos {file_extension} já criada!") if os.path.exists(name) else (os.makedirs(name, exist_ok= True), 
                                                                                                       logger.info(f"Pasta para inserção dos arquivos {file_extension} criada com sucesso!"))
        except Exception as e:
            logger.info(f"Erro ao criar a pasta para os arquivos {file_extension}: {e}")

    arquivos = os.listdir(source_dir)
    for arquivo in arquivos: 
        caminho_completo = os.path.join(source_dir, arquivo)
        print(f"Caminho completo do arquivo: {caminho_completo}")
        if os.path.isfile(caminho_completo) and arquivo.endswith('.csv'): 
            df = pd.read_csv(caminho_completo)
            file_name = os.path.basename(caminho_completo).split('.')[0]
            print(f"Nome do arquivo: {file_name}")

            # Salvando o arquivo no formato Json.
            json_file = os.path.join(output_dir, "json/",f"{file_name}.json")
            df.to_json(path_or_buf= json_file, orient="records", lines= False)
            print("Arquivo Json foi salvo com sucesso!")

            # Salvando o arquivo no formato Parquet.
            parquet_file = os.path.join(output_dir, "parquet/",f"{file_name}.parquet")
            table = pa.Table.from_pandas(df)
            pq.write_table(table, parquet_file)
            print("Arquivo Parquet foi salvo com sucesso!")

            logger.info(f"Arquivos Json e Parquet salvos com sucesso!\nJson: {os.path.join(output_dir, "json/")}\nParquet: {os.path.join(output_dir, "parquet/")}")

        else: 
            print(f"Arquivo '.txt' não processado!\n{caminho_completo}")
            logger.info(f"Arquivo '.txt' não processado!\n{caminho_completo}")

    return None

def upload_parquet_s3(settings: dict) -> None:
    # Configurando o Cliente do S3
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id= settings['aws_access_key_id'],
            aws_secret_access_key= settings['aws_secret_access_key'],
            region_name= settings['region_name']
        )
        print("Cliente S3 configurado com sucesso.")         
        logger.info("Cliente S3 configurado com sucesso.")     
    except Exception as e:
        print(f"Erro ao configurar o cliente S3: {e}")
        logger.info(f"Erro ao configurar o cliente S3: {e}")
        raise

    # Caminho dos arquivos a serem enviados 
    parquet_files = os.path.join(os.getcwd(), "files/data/output_files/parquet/")

    bucket_name  = settings['bucket_name']
    arquivos = os.listdir(parquet_files)
    for arquivo in arquivos: 
        caminho_completo = os.path.join(parquet_files, arquivo)
        try:
            print(f"Tentando fazer upload de '{arquivo}' para o bucket '{bucket_name}'...")
            s3_client.upload_file(caminho_completo, bucket_name, 'parquet/' + arquivo)
            print(f"{arquivo} foi enviado para o S3.")
            logger.info(f"{arquivo} foi enviado para o S3.")
        except Exception as e:
            print(f"Erro ao enviar '{arquivo}' para o S3: {e}")
            logger.info(f"Erro ao enviar '{arquivo}' para o S3: {e}")
            raise
    
    print("Processo de Upload finalizado!")

def delete_source_files(path_list: list) -> None:
    # Caminho dos arquivos a serem deletados 
    source_files = path_list[0]

    arquivos = os.listdir(source_files)
    for arquivo in arquivos: 
        caminho_completo = os.path.join(source_files, arquivo)
        try:
            print(f"Deletando o arquivo: '{arquivo}' data pasta: '{source_files}'...")
            os.remove(caminho_completo)
            print(f"{arquivo} deletado com sucesso.")
            logger.info(f"{arquivo} deletado com sucesso.")
        except Exception as e:
            print(f"Erro ao deletar o '{arquivo}'. Erro: {e}")
            logger.info(f"Erro ao deletar o '{arquivo}'. Erro: {e}")
            raise