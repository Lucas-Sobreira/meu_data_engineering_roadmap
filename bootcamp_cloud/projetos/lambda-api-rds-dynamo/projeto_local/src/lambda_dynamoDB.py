import requests
import json
import os
import boto3
from decimal import Decimal
from time import gmtime, strftime

# Criar o objeto DynamoDB usando o SDK boto3
dynamodb = boto3.resource('dynamodb')
# Selecionar a tabela que criamos
table = dynamodb.Table('CryptoCurrency')

# Carregar variáveis de ambiente
url = os.getenv('API_URL')  # URL da API obtida das variáveis de ambiente
api_key = os.getenv('CMC_API_KEY')  # Chave da API obtida das variáveis de ambiente

# Parâmetros da requisição para obter a cotação do Bitcoin
parameters = {
    'symbol': 'BTC,ETH,SOL,DOGE',  # Identificando o Bitcoin pelo símbolo
    'convert': 'BRL'  # Convertendo a cotação para USD
}

# Headers com a chave da API
headers = {
    'Accept': 'application/json',
    'X-CMC_PRO_API_KEY': api_key  # Obtendo a chave da API das variáveis de ambiente
}

# Função para coletas as Crypto Moedas
def get_brl_quotes():
    try:
        # Criar uma sessão para gerenciar as requisições
        with requests.Session() as session:
            # Configurar os headers da sessão
            session.headers.update(headers)

            # Fazer o request GET para a API com parâmetros
            response = session.get(url, params=parameters)
            response.raise_for_status()  # Levanta um erro se o status code for 4xx ou 5xx

            data = response.json()  # Carregar a resposta JSON

            criptos = {'BTC', 'DOGE', 'ETH', 'SOL'}

            # Verificar se os dados do Bitcoin estão presentes na resposta
            if data.get('data') and all(crypto in data['data'] for crypto in criptos):
                brl_quotes = []
                for symbol in criptos:
                    crypto_data = data['data'][symbol]
                    brl_quote = crypto_data['quote']['BRL']
                    brl_crypto = {
                        'CurrencyId': crypto_data['symbol'] + '_' + strftime("%Y%m%d%H%M%S", gmtime()), # PK = Crypto + Date
                        'symbol': crypto_data['symbol'],
                        'price': Decimal(str(brl_quote['price'])),
                        'volume_24h': Decimal(str(brl_quote['volume_24h'])),
                        'market_cap': Decimal(str(brl_quote['market_cap'])),
                        'fully_diluted_market_cap': Decimal(str(brl_quote['fully_diluted_market_cap'])),
                        'last_updated': brl_quote['last_updated']
                    }
                    brl_quotes.append(brl_crypto)
                return brl_quotes
            else:
                print("Erro ao obter a cotação das crypto moedas:", data.get('status', {}).get('error_message', 'Erro desconhecido'))
                return None
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

# Função Lambda que realiza o sorteio e persiste os dados
def load_dynamoDB(brl_quotes):
    if brl_quotes:
        # Salvar os dados no DynamoDB
        for quote in brl_quotes:
            response = table.put_item(Item=quote)
            print(f"Item {quote['symbol']} salvo com sucesso. Response: {response}")
        return True
    else:
        print("Nenhum dado de cotação para salvar no DynamoDB.")
        return False

# Função Lambda que organiza o pipeline
def lambda_handler(event, context):
    brl_quotes = get_brl_quotes()
    if brl_quotes:
        load_DB = load_dynamoDB(brl_quotes)
        if load_DB:
            # Converter os objetos Decimal para string antes de serializar para JSON
            brl_quotes_serializable = []
            for quote in brl_quotes:
                quote_serializable = quote.copy()
                for key, value in quote_serializable.items():
                    if isinstance(value, Decimal):
                        quote_serializable[key] = str(value)
                brl_quotes_serializable.append(quote_serializable)

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Dados das crypto moedas coletados e salvos no DynamoDB com sucesso!',
                    'brl_quotes': brl_quotes_serializable
                })
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': 'Erro ao salvar os dados no DynamoDB.'
                })
            }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Erro ao obter as cotações das crypto moedas.'
            })
        }