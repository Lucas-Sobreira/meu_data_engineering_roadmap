import requests
from pydantic import BaseModel

class PokemonSchema(BaseModel): # Contrato de Dados, Schema de Dados
    name: str
    type: str

    class Config: 
        # orm_mode = True
        from_attributes = True

def pegar_pokemon(id: int) -> PokemonSchema: 
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}")

    data = response.json()
    data_types = data['types']
    type_list = []

    # Coletando apenas o nome dos tipos de pokemon
    for type_info in data_types: 
        type_list.append(type_info['type']['name'])

    # Retirando da lista, transformando em uma String com virgula
    types = ', '.join(type_list)
    return PokemonSchema(name= data['name'], type= types)

if __name__ == "__main__": 
    pokemon = pegar_pokemon(30)
    print(pokemon)