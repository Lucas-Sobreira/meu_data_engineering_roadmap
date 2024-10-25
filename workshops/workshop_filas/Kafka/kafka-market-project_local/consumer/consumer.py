import time
import random
from confluent_kafka import Consumer, KafkaError
import json
import os
from dotenv import load_dotenv 
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Função para configurar o Consumer
def load_consumer_settings(): 
    # Carregar variáveis de ambiente do arquivo .env 
    load_dotenv()

    consumer_conf = {
        'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS'],
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': os.environ['SASL_USERNAME'],
        'sasl.password': os.environ['SASL_PASSWORD'],
        'group.id': 'temperature-consumer-group',
        'auto.offset.reset': 'earliest'
    }

    topic_name = os.getenv('TOPIC')

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic_name])

    return consumer

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
    return connection_string

def consume_messages(consumer):
    batch_size = 2  # Número de mensagens para processar por batch
    batch_interval = 5  # Intervalo de tempo (em segundos) entre os batches
    messages = []
    start_time = time.time()  # Inicializa start_time dentro da função

    try:
        while True:
            print('Esperando mensagem')
            msg = consumer.poll(1.0)  # Espera até 1 segundo por uma nova mensagem
            if msg is None:
                continue
            if msg.error():
                continue

            value = json.loads(msg.value().decode('utf-8'))  # Converte o valor para JSON
            # Desnormalizar a mensagem
            data = {
                'id': value['id'],
                'latitude': value['latitude'],
                'longitude': value['longitude'],
                'temperature': value['temperature'],
                'time': datetime.now()  # Captura o tempo atual da mensagem
            }
            messages.append(data)

            print(f"printando mensagens: {messages}")

            # Processar batch quando atingir o tamanho ou o intervalo de tempo
            if len(messages) >= batch_size or (time.time() - start_time) >= batch_interval:
                df = pd.DataFrame(messages)
                df.to_sql('temperature_data', engine, if_exists='append', index=False)
                messages = []  # Limpar lista de mensagens após salvar no banco
                start_time = time.time()  # Resetar o contador de tempo

    except KeyboardInterrupt:
        pass
    finally:
        print("Closing consumer.")
        consumer.close()

if __name__ == "__main__":
    # Setando a String de Conexão com o Postgres Render
    SQLALCHEMY_DATABASE_URL = postgres_connection()
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    # Consome os dados do Confluent Kafka e Armazena no Postgres Render
    consumer = load_consumer_settings()
    consume_messages(consumer)