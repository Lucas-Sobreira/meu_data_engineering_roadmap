import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# PostgreSQL Settings
def load_postgres_settings(): 
    """
    Carrega as configurações a partir de variáveis de ambiente.
    """
    settings = {
        "db_host": os.environ["POSTGRES_HOST"],
        "db_user": os.environ["POSTGRES_USER"],
        "db_pass": os.environ["POSTGRES_PASSWORD"],
        "db_name": os.environ["POSTGRES_DB"],
        "db_port": os.environ["POSTGRES_PORT"],
    }
    return settings

# Postgres String Connection
def postgres_connection():
    """
    Carrega as configurações a partir de variáveis de ambiente.
    """
    settings = load_postgres_settings()
    connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"
    engine = create_engine(connection_string)    
    return engine

# Load the data from PostgreSQL Render
def load_data():
    """
    Carrega os dados que foram armazenados no Postgres Render pelo consumer kafka
    """
    engine = postgres_connection()
    query = '''
        SELECT symbol, price, volume_24h, market_cap, fully_diluted_market_cap, last_updated FROM cryptocurrency
    '''
    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()  # Return an empty Dataframe if error

# Rewriting Dataframe
def rewrite_df(df):
    """
    Reestruturando os dados para construção do Dash
    """
    df_dash = df[['symbol', 'price', 'last_updated']]
    df_dash['last_updated'] = pd.to_datetime(df_dash['last_updated']).dt.strftime('%Y-%m-%d %H:%M:%S')
    return df_dash

# Streamlit building part. Show the Dashboard and Dataframe base.
def display_data(df, df_dash):
    """
    Parte visual do Dataframe e Dashboard, utilizando Streamlit.
    """
    # Use the full page instead of a narrow central column
    st.set_page_config(layout="wide")

    st.title("CriptoCurrencies Historical")

    # Dataframe and Dashboard Side By Side
    # col1, col2 = st.columns(2)
    col1, spacer, col2 = st.columns([7, 1, 3])  # DataFrame mais largo que a legenda

    with col1: 
        st.subheader("Dataframe")
        st.dataframe(df.head())

    with col2:
        st.subheader("Legenda")
        st.markdown("""
            <ul>
                <li><b>symbol</b>: The cryptocurrency symbol;</li>
                <li><b>price</b>: Latest average trade price across markets;</li>
                <li><b>volume_24h</b>: 24 hour trading volume for each currency;</li>
                <li><b>market_cap</b>: market cap (latest trade price x circulating supply);</li>
                <li><b>fully_diluted_market_cap</b>: Is the estimated value of a cryptocurrency if all of its tokens were in circulation;</li>
                <li><b>last_updated</b>: Time of last update;</li>
            </ul>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Dashboard")
    fig = px.line(df_dash, x="last_updated", y="price", color="symbol", height=500)
    st.plotly_chart(fig)    
    return None

if __name__ == '__main__':
    # Carregando os dados do .env
    load_dotenv()

    # Load the data from PostgreSQL RDS
    df = load_data()

    # Rewrite de Dataframe Base to an easier Dataframe to plot.
    df_dash = rewrite_df(df)

    display_data(df, df_dash)