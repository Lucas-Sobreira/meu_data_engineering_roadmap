import pandas as pd
import os 
import glob 
from utils.log import log_decorator

@log_decorator
def extrair_dados_e_consolidar(pasta: str) -> pd.DataFrame:
    """
    Extrair e consolidar os Dados vindo dos Jsons (API)
    """
    arquivos_json = glob.glob(os.path.join(pasta, '*.json'))
    df_list = [pd.read_json(arquivo) for arquivo in arquivos_json]
    df_total = pd.concat(df_list, ignore_index=True)
    return df_total

@log_decorator
def calcular_kpi_total_vendas(dados: pd.DataFrame) -> pd.DataFrame: 
    """
    Calcula o KPI do total de vendas. Quantidade * Venda
    """
    df_final = dados.copy()
    df_final['Total'] = dados['Quantidade'] * dados['Venda']
    return df_final

@log_decorator
def formato_arquivo(escolha_formato: str, df: pd.DataFrame) -> None:
    """
    Através do input de escolha de Save Formato do Usuário, chama a função para salvar os dados!
    """ 
    if escolha_formato == 'Dois': 
        carregar_dados(df = df, formato_csv = True, formato_parquet = True)
    elif escolha_formato == 'CSV': 
        carregar_dados(df = df, formato_csv = True)
    elif escolha_formato == 'Parquet':
        carregar_dados(df = df, formato_parquet = True)
    else: 
        carregar_dados(df = df)

@log_decorator
def carregar_dados(df: pd.DataFrame, path: str = './save_data/', formato_csv:bool = False, formato_parquet:bool = False) -> None: 
    if (formato_csv == True) & (formato_parquet == True): 
        df.to_csv(path + 'dados.csv')
        df.to_parquet(path + 'dados.parquet')        
    elif formato_parquet == True: 
        df.to_parquet(path + 'dados.parquet')
    elif formato_csv == True: 
        df.to_csv(path + 'dados.csv')
    else: 
        print('Nenhum formato de arquivo definido!\nFavor escolher CSV, Parquet ou os dois!')

@log_decorator
def pipeline_calcular_kpi_de_vendas_consolidado(pasta: str) -> None: 
    df_total = extrair_dados_e_consolidar(pasta)
    df_final = calcular_kpi_total_vendas(df_total)
    escolha_formato = str(input('Escolha um dos formatos para salvar o arquivo consolidado e com calculo de KPI. Digite: CSV, Parquet ou Dois\n'))
    formato_arquivo(escolha_formato, df_final)