from loguru import logger

# Basta trocar o print pelo logger
# print -> logger

logger.add("meu_app.log", level="CRITICAL")

def soma(x, y): 
    try: 
        soma = x + y
        logger.info(f'Variáveis informadas para a função de soma: {x} e {y}.')
        logger.info(f'O valor da soma desses valores é de: {soma}')
        return soma
    except: 
        logger.critical(f'Foi informado algum valor indevido para a função de soma.')
        logger.info(f'Valores informados: {x} e {y}')

logger.info(soma(2, 5))
logger.info(soma(2, 'I'))