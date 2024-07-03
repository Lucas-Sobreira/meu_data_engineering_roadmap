import pandas as pd 

df = pd.read_csv('exemplo.csv')
df_filtrado = df.query("estado == 'SP'")
print(df_filtrado)