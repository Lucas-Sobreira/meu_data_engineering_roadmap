from airflow.decorators import dag, task
from airflow.operators.python import BranchPythonOperator
from src.parquet_s3 import verifica_arquivos_source, load_settings, configurando_ambiente, arquivos_output, upload_parquet_s3, delete_source_files
from datetime import datetime

@dag(
    dag_id="pipeline_s3_parquet",
    description="Envio de arquivos locais no formato parquet para o Bucket S3 da AWS.",
    schedule="0 * * * *",  # CRON ajustado para rodar diariamente
    start_date=datetime(2025, 2, 24),
    catchup=False
)
def pipeline_parquet_s3():
    """
    1. Verifica se há arquivos na pasta 'source';
    2. Se houver arquivos, inicia o pipeline;
    3. Caso contrário, encerra a execução e aguarda a próxima tentativa.

    Fluxo do Pipeline:
        1. Lê variáveis de ambiente do .env;
        2. Configura ambiente e diretórios;
        3. Gera e salva arquivos Parquet na pasta 'output';
        4. Faz upload dos arquivos para o S3;
        5. Remove os arquivos originais da pasta 'source'.
    """

    def decide_proximo_passo():
        """ Decide se o DAG deve continuar ou encerrar """
        if verifica_arquivos_source():
            return "load_settings"  # Continua o fluxo normalmente
        else:
            return "fim_processo"   # Interrompe o DAG sem erro

    verifica_arquivos = BranchPythonOperator(
        task_id="verifica_arquivos_source",
        python_callable=decide_proximo_passo
    )

    @task(task_id='fim_processo')
    def task_fim_processo():
        """ Tarefa vazia para encerrar o DAG se não houver arquivos """
        print("🚫 Nenhum arquivo encontrado. Encerrando DAG.")

    @task(task_id='load_settings')
    def task_load_settings():
        print("🔍 Lendo variáveis do '.env'")
        return load_settings()

    @task(task_id='configurando_ambiente')
    def task_configurando_ambiente():
        print("🛠️ Configurando ambiente e diretórios...")
        return configurando_ambiente()
    
    @task(task_id='lista_arquivos_destino')
    def task_arquivos_destino(path_list: list):
        print("📂 Criando arquivos Parquet na pasta 'Output'")
        return arquivos_output(path_list)

    @task(task_id='upload_parquet_s3')
    def task_upload_parquet_s3(settings: dict):
        print("📤 Enviando arquivos Parquet para o S3...")
        return upload_parquet_s3(settings)
    
    @task(task_id='delete_source_files')
    def task_delete_source_files(path_list: list):
        print("🗑️ Removendo arquivos originais da pasta 'Source'")
        return delete_source_files(path_list)

    # Caso não contenha arquivos irá esperar a próxima "rodada"
    fim = task_fim_processo()

    # Definição do fluxo de execução    
    t1 = task_load_settings()               # Carrega variáveis do .env
    t2 = task_configurando_ambiente()       # Configura ambiente
    t3 = task_arquivos_destino(t2)          # Gera arquivos na pasta output
    t4 = task_upload_parquet_s3(t1)         # Upload para S3 (depende de t1 e t3)
    t5 = task_delete_source_files(t2)       # Remove arquivos da source (depende de t2 e t3)

    # Lógica de Branching
    verifica_arquivos >> [t1, fim]  # Se houver arquivos, continua para t1; senão, encerra

    # Encadeamento correto das tarefas
    t1 >> t2 >> t3
    t3 >> [t4, t5]  # Upload e delete acontecem em paralelo

pipeline_parquet_s3()