import pandas as pd 

class CsvProcessor:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.df = None
        self.df_filtrado = None

    def carrega_csv(self): 
        self.df = pd.read_csv(self.file_path)

    def filtra_por(self, coluna: str, atributo: str):
        self.df_filtrado = self.df.query(f"{coluna} == '{atributo}'")
        return self.df_filtrado.reset_index(drop=True)
    
    def sub_filtro(self, coluna: str, atributo: str, operacao: str):
        self.df_filtrado = self.df_filtrado.query(f"{coluna} {operacao} '{atributo}'")
        return self.df_filtrado.reset_index(drop=True)