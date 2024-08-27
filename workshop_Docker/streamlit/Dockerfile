# Instalando o python + poetry
FROM python:3.12
RUN pip install poetry 

# Copiando todos o conteúdo do meu computador para o /src Docker
COPY . /src 

# Entrando na pasta do /src dentro do Docker
WORKDIR /src

RUN poetry install

# Expondo a porta 8501 e rodando o código Streamlit
EXPOSE 8501
ENTRYPOINT ["poetry", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]