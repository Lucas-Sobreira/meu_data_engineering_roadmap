from confluent_kafka import Producer
from dotenv import load_dotenv 
import os 
import random 
import time 

# Carregar variáveis de ambiente do arquivo .env 
load_dotenv()

# Configurações do produtor
conf = {
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVERS'),
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': os.getenv('SASL_USERNAME'),
    'sasl.password': os.getenv('SASL_PASSWORD')
}

producer = Producer(**conf)

# Função de callback para entrega de mensagens
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Produção de mensagens simulando um sensor de geladeira
topic = os.getenv('TOPIC')

for i in range(10):
    temperature = random.uniform(-10, 30)  # Temperatura aleatória entre -10 e 30 graus Celsius
    key = f"sensor{i % 3}"  # Usar diferentes chaves para distribuir entre partições
    producer.produce(topic, key=key, value=f"{temperature:.2f}", callback=delivery_report)
    producer.poll(0) # armazena uma quantidade de mensagens antes de enviar para o Broker
    time.sleep(1)  # Simula leitura de temperatura a cada segundo

# Espera até todas as mensagens serem entregues
producer.flush()