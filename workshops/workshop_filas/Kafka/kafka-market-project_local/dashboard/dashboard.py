import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import time
import plotly.express as px

# Configuração do PostgreSQL
def load_postgres_settings(): 
    """
    Carrega as configurações a partir de variáveis de ambiente.
    """
    # Carregar variáveis de ambiente do arquivo .env 
    load_dotenv()

    settings = {
        "db_host": os.getenv("POSTGRES_HOST"),
        "db_user": os.getenv("POSTGRES_USER"),
        "db_pass": os.getenv("POSTGRES_PASSWORD"),
        "db_name": os.getenv("POSTGRES_DB"),
        "db_port": os.getenv("POSTGRES_PORT"),
    }
    return settings

# Retorna a String de Conexão Postgres
def postgres_connection():
    settings = load_postgres_settings()
    connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"
    engine = create_engine(connection_string)    
    return engine

# Função para carregar dados do banco de dados
def load_data():
    engine = postgres_connection()
    query = """
    SELECT DISTINCT ON (id) *
    FROM temperature_data
    ORDER BY id, time DESC;
    """
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

# Função para exibir o mapa
def display_map(df):
    df['color'] = df['temperature'].apply(lambda x: 'red' if x > 5 else 'blue')
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="color",
        color_discrete_map={"red": "red", "blue": "blue"},
        hover_name="id",
        hover_data={"temperature": True, "latitude": False, "longitude": False},
        zoom=3,
        height=600,
    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig)

# Loop para atualizar a página a cada 5 segundos
while True:
    st.title('Dashboard de Temperaturas')
    data = load_data()
    if not data.empty:
        st.write(data)
        display_map(data)
    else:
        st.write('A tabela "temperature_data" ainda não existe ou não foi possível carregar os dados.')
    
    time.sleep(10)
    st.experimental_rerun