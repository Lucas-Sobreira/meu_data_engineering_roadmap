import requests
from db import SessionLocal, engine, Base
from models import Pokemon
from schema import PokemonSchema

Base.metadata.create_all(bind=engine)

# Coletando os dados da APIe validando-os com Pydantic
def fetch_pokemon_data(pokemon_id: int) -> PokemonSchema:
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    if response.status_code == 200:
        data = response.json()
        types = ', '.join(type['type']['name'] for type in data['types'])
        return PokemonSchema(name= data['name'], type= types)
    else:
        return None

# Adicionando os dados, já validados, no Banco de Dados
def add_pokemon_to_db(pokemon_schema: PokemonSchema) -> Pokemon:
    with SessionLocal() as db:
        db_pokemon = Pokemon(name= pokemon_schema.name, type= pokemon_schema.type)
        db.add(db_pokemon)
        db.commit()
        db.refresh(db_pokemon)
    return db_pokemon