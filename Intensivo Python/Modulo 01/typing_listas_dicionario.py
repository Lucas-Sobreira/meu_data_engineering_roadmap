# Crie um dicionário para armazenar informações de um livro, 
# incluindo título, autor e ano de publicação. Imprima cada informação. 

from typing import Dict

titulo: str = 'Game of Thrones'
autor: str = 'Estagiario'
ano_publicacao: int = 2005

livro_01: Dict[str, int] = {
    "Título": titulo, 
    "Autor": autor, 
    "Ano Publicação": ano_publicacao
}

livro_02: Dict[str, int] = {
    "Título": titulo, 
    "Autor": autor, 
    "Ano Publicação": 2007
}

dict_livros: dict= {
    'livro_01': livro_01,
    'livro_02': livro_02
}

# print(dict_livros.items())

for dict in dict_livros.items(): 
    print(dict[-1]['Ano Publicação'])