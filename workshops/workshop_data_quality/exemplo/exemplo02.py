import pandas as pd 
import pandera as pa
from pandera import Check, Column, DataFrameSchema

# Escrevendo o DataFrame referência
df = pd.DataFrame({
    "column1": [5, 10, 20], 
    "column2": ["a", "b", "c"],
    "column3": pd.to_datetime(["2010", "2011", "2012"])
})

# Inferindo o Schema da tabela acima
schema = pa.infer_schema(df)
# print(schema)

# Salvando o Schema do DataFrame em um arquivo JSON
with open("inferred_schema.json", "w") as file:
    file.write(schema.to_script())