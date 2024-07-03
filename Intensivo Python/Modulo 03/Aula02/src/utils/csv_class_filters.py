import pandas as pd 

class CsvProcessor:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.df = None
        self.df_filtrado = None

    def carrega_csv(self): 
        self.df = pd.read_csv(self.file_path)

    def filtra_por(self, colunas: list, atributos: list):
        if len(colunas) != len(atributos): 
            raise ValueError("Não tem o mesmo número de colunas e atributos")

        elif len(colunas) == 0:
            return self.df
        
        coluna_atual = colunas[0]
        atributo_atual = atributos[0]

        df_filtrado = self.df.query(f"{coluna_atual} == '{atributo_atual}'")

        if len(colunas) == 1:
            return df_filtrado
        else: 
            return self.filtra_por(colunas[1:], atributos[1:])