import os 
from pathlib import Path
from dotenv import load_dotenv
from typing import List

import logging
from datetime import datetime

import pandas as pd  
import pyarrow as pa
import pyarrow.parquet as pq
import boto3

def load_settings() -> dict: 
    """
    Carrega as configurações a partir de variáveis de ambiente.
    """
    dotenv_path = Path.cwd() / '.env'
    load_dotenv(dotenv_path = dotenv_path)

    settings = {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region_name": os.getenv("REGION_NAME"),
        "bucket_name": os.getenv("BUCKET_NAME"),
        "s3_key": os.getenv("S3_KEY")
    }
    return settings

def config_s3(settings: dict) -> str:
    """
        Configura o Client do S3
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id= settings['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key= settings['AWS_SECRET_ACCESS_KEY'],
            region_name= settings['REGION_NAME']
        )
        logging.info("Cliente S3 configurado com sucesso.")
        return s3_client        
    
    except Exception as e:
        logging.info(f"Erro ao configurar o cliente S3: {e}")
        raise

def lista_arquivos(source_folder: str) -> List[str]: 
    """
        Lista os arquivos da pasta Souce e filtra de acordo com a extensão. 
    """
    arquivos: List[str] = []
    try: 
        for arquivo in os.listdir(source_folder):
            caminho_completo = os.path.join(source_folder, arquivo)
            if os.path.isfile(caminho_completo) and arquivo.endswith('.csv'): 
                arquivos.append(caminho_completo)
        logging.info(f"Arquivos listados na pasta '{source_folder}': {arquivos}")
    except Exception as e:
        logging.info(f"Erro ao listar arquivos na pasta '{source_folder}': {e}")
        raise
    return arquivos

def check_dir(output_dir: str) -> None:
    """
        Checa se o diretório já foi criado ou se terá que ser criado, de acordo com as extensões dos arquivos.
    """
    extensions = ["json", "parquet"]

    for file_extension in extensions:
        try: 
            name= output_dir + f"{file_extension}/"
            logging.info(f"Pasta para os arquivos {file_extension} já criada!") if os.path.exists(name) else (os.makedirs(name, exist_ok= True), 
                                                                                                       logging.info(f"Pasta para inserção dos arquivos {file_extension} criada com sucesso!"))
        except Exception as e:
            logging.info(f"Erro ao criar a pasta para os arquivos {file_extension}: {e}")
            raise

def arquivos_output(output_dir: str, path_csv: str) -> None:
    """
        Realiza a transformação de CSV para Json e Parquet dos arquivos e salva na pasta destino.
        Caso a pasta ainda não exista, será criada.
    """

    df = pd.read_csv(path_csv)
    file_name = os.path.basename(path_csv)

    # Salvando o arquivo no formato Json.
    json_file = os.path.join(output_dir, "json/",f"{file_name}.json")
    df.to_json(path_or_buf= json_file, orient="records", lines= False)

    # Salvando o arquivo no formato Parquet.
    parquet_file = os.path.join(output_dir, "parquet/",f"{file_name}.parquet")
    table = pa.Table.from_pandas(df)
    pq.write_table(table, parquet_file)

def upload_arquivos_para_s3(arquivos: List[str], s3_client, buckt_name: str) -> None:
    """
        Faz o upload dos arquivos .parquet para o S3.
    """
    for arquivo in arquivos:
        nome_arquivo: str = os.path.basename(arquivo)
        try:
            logging.info(f"Tentando fazer upload de '{nome_arquivo}' para o bucket '{buckt_name}'...")
            # s3_client.upload_file(arquivo, buckt_name, nome_arquivo)
            logging.info(f"{nome_arquivo} foi enviado para o S3.")
        except Exception as e:
            logging.info(f"Erro ao enviar '{nome_arquivo}' para o S3: {e}")
            raise

def deletar_arquivos_locais(source_dir: str, arquivos: List[str]) -> None:
    """
        Deletando os arquivos locais, que foram salvos no formato .parquet no S3.
    """
    for arquivo in arquivos:
        try:
            caminho_completo = os.path.join(source_dir, arquivo)
            os.remove(caminho_completo)
            logging.info(f"{arquivo} foi deletado da pasta local.")
        except Exception as e:
            logging.info(f"Erro ao deletar o arquivo '{arquivo}': {e}")

def pipeline(source_dir: str, output_dir: str) -> None:
    """
        Essa é a função principal, na qual irá rodar todo o Pipeline dos Dados. 
            - Ler as variáveis de ambiente, do arquivo .env;
            - Configurar o Cliente do S3;
            - Listar os arquivos da pasta source; 
            - Verifica se a pasta dos arquivos "output", os arquivos que serão carregados no S3, existe ou se será criada;
            - Salva os arquivos nos formatos Parquet e Json, para fins de comparação de tamanho;
            - Realiza o Upload dos arquivos .parquet para o S3;
            - Deleta os arquivos da pasta Source, ou seja, os arquivos originais. Uma vez que os dados já estão na Cloud (S3);
    """
    # Carrega as váriaveis de ambiente
    settings = load_settings()

    # Configura o Client do S3
    s3_client = config_s3(settings)

    # Lista os arquivos na pasta Source
    arquivos = lista_arquivos(source_dir)

    # Checa se o diretório já foi criado ou se terá que ser criado
    check_dir(output_dir)

    # Salvando os arquivos no formato Json e Parquet
    for arquivo in arquivos: 
        arquivos_output(output_dir, path_csv = arquivo)
    logging.info("Arquivos Json e Parquet salvos na pasta destino.")

    # Realiza o upload dos arquivos para o S3 
    arquivos = os.listdir(output_dir + "parquet/")
    bucket_name = settings['bucket_name']
    upload_arquivos_para_s3(arquivos, s3_client, bucket_name)

    # Deleta os arquivos da pasta Source
    logging.info("Deletando os arquivos locais")
    arquivos_locais = os.listdir(source_dir)
    deletar_arquivos_locais(source_dir, arquivos= arquivos_locais)

    logging.info("Arquivos devidamente transformados e Salvos no S3! Prontos para consumo do Glue e Athena.")

if __name__ == "__main__":
    # Configuração do arquivo de log
    datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    logging.basicConfig(filename=f'./logs/app_{datetime_now}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

    # Pastas de arquivos
    source_dir = "./data/source/"
    output_dir = "./data/output_files/"

    # Rodando o Pipeline de Dados
    if os.listdir(source_dir) != []:
        logging.info("Rodando o Pipeline de Dados para envio ao S3.")
        pipeline(source_dir, output_dir)
    else: 
        logging.info("Não existem arquivos no diretório source.")