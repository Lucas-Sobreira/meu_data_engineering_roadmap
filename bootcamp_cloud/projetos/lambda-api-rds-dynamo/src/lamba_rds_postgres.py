import requests
import json
import os
from decimal import Decimal
from time import gmtime, strftime
from sqlalchemy import create_engine, Column, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from typing import List, Dict, Optional

# Carregar variáveis de ambiente
url = os.getenv('API_URL')  # URL da API
api_key = os.getenv('CMC_API_KEY')  # Chave da API
db_url = os.getenv('DATABASE_URL')  # URL do banco de dados PostgreSQL

# Verificar se as variáveis de ambiente estão definidas
if not all([url, api_key, db_url]):
    raise EnvironmentError("Por favor, defina as variáveis de ambiente API_URL, CMC_API_KEY e DATABASE_URL.")

# Parâmetros da requisição para obter a cotação das criptomoedas
parameters = {
    'symbol': 'BTC,ETH,SOL,DOGE',
    'convert': 'BRL'
}

# Headers com a chave da API
headers = {
    'Accept': 'application/json',
    'X-CMC_PRO_API_KEY': api_key
}

# Declarar o modelo da tabela usando o sistema declarativo do SQLAlchemy
Base = declarative_base()

class CryptoCurrency(Base):
    """
    Modelo da tabela para armazenar dados de criptomoedas.
    """
    __tablename__ = 'cryptocurrency'

    currency_id = Column(String, primary_key=True)  # Mantido como String para flexibilidade
    symbol = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    volume_24h = Column(Numeric, nullable=False)
    market_cap = Column(Numeric, nullable=False)
    fully_diluted_market_cap = Column(Numeric, nullable=False)
    last_updated = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False) # Adicionado created_at

    def __repr__(self):
        return (f"<CryptoCurrency(currency_id='{self.currency_id}', symbol='{self.symbol}', "
                f"price={self.price}, volume_24h={self.volume_24h}, market_cap={self.market_cap})>")

# Configurar o motor do SQLAlchemy e criar a sessão
engine = create_engine(db_url)
Base.metadata.create_all(engine)  # Cria as tabelas no banco de dados
Session = sessionmaker(bind=engine)
session = Session()

def get_brl_quotes() -> Optional[List[Dict]]:
    """
    Obtém as cotações das criptomoedas da API.

    Retorna:
        Optional[List[Dict]]: Uma lista de dicionários contendo os dados das cotações, ou None em caso de erro.
    """
    try:
        with requests.Session() as http_session:
            http_session.headers.update(headers)
            response = http_session.get(url, params=parameters)
            response.raise_for_status()  # Lança uma exceção para códigos de status HTTP ruins (4xx ou 5xx)
            data = response.json()

            criptos = {'BTC', 'DOGE', 'ETH', 'SOL'}
            if data.get('data') and all(crypto in data['data'] for crypto in criptos):
                brl_quotes = []
                for symbol in criptos:
                    crypto_data = data['data'][symbol]
                    brl_quote = crypto_data['quote']['BRL']
                    # Usando um timestamp em microssegundos para maior precisão na CurrencyId
                    currency_id = f"{crypto_data['symbol']}_{strftime('%Y%m%d%H%M%S', gmtime())}"
                    brl_crypto = {
                        'currency_id': currency_id,
                        'symbol': crypto_data['symbol'],
                        'price': Decimal(str(brl_quote['price'])),
                        'volume_24h': Decimal(str(brl_quote['volume_24h'])),
                        'market_cap': Decimal(str(brl_quote['market_cap'])),
                        'fully_diluted_market_cap': Decimal(str(brl_quote['fully_diluted_market_cap'])),
                        'last_updated': brl_quote['last_updated']  # Mantendo o formato original da API
                    }
                    brl_quotes.append(brl_crypto)
                return brl_quotes
            else:
                print("Erro ao obter a cotação das criptomoedas:", data.get('status', {}).get('error_message', 'Erro desconhecido'))
                return None
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

def load_postgres(brl_quotes: List[Dict]) -> bool:
    """
    Salva os dados das cotações no banco de dados PostgreSQL usando SQLAlchemy.

    Args:
        brl_quotes (List[Dict]): Lista de dicionários contendo os dados das cotações.

    Retorna:
        bool: True se os dados foram salvos com sucesso, False em caso de erro.
    """
    if not brl_quotes:
        print("Nenhum dado de cotação para salvar no banco de dados.")
        return False
    try:
        for quote in brl_quotes:
            # Converter o dicionário para uma instância do modelo CryptoCurrency
            crypto_data = CryptoCurrency(
                currency_id=quote['currency_id'],
                symbol=quote['symbol'],
                price=quote['price'],
                volume_24h=quote['volume_24h'],
                market_cap=quote['market_cap'],
                fully_diluted_market_cap=quote['fully_diluted_market_cap'],
                last_updated=quote['last_updated']
            )
            session.add(crypto_data) # Adiciona o objeto à sessão
        session.commit() # Commita a transação
        print("Dados das criptomoedas salvos com sucesso no PostgreSQL.")
        return True
    except Exception as e:
        session.rollback() # Em caso de erro, faz rollback da transação
        print(f"Erro ao salvar os dados no PostgreSQL: {e}")
        return False
    finally:
        session.close() # Garante que a sessão seja fechada

def lambda_handler(event, context) -> Dict:
    """
    Função Lambda principal para coletar e salvar dados de criptomoedas no PostgreSQL.

    Args:
        event (dict): Dados do evento da Lambda (não utilizado neste caso).
        context (object): Contexto da execução da Lambda.

    Retorna:
        Dict: Um dicionário contendo o status da operação e os dados das cotações.
    """
    brl_quotes = get_brl_quotes() # Obtem os dados da API
    if brl_quotes:
        saved = load_postgres(brl_quotes) # Salva no DB
        if saved:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Dados das criptomoedas coletados e salvos no PostgreSQL com sucesso!',
                    'brl_quotes': brl_quotes
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': 'Erro ao salvar os dados no PostgreSQL.'
                })
            }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Erro ao obter as cotações das criptomoedas.'
                })
            }
