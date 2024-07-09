import time 
import random
from controller import fetch_pokemon_data, add_pokemon_to_db

def main():
    while True: 
        pokemon_id = random.randint(1, 350) # Gera um ID aleatório entre 1 e 350
        pokemon_schema = fetch_pokemon_data(pokemon_id)
        if pokemon_schema: 
            print("Adicionando ao Banco: {}".format(pokemon_schema.name))
            add_pokemon_to_db(pokemon_schema)
        else: 
            print("Não foi possível obter os dados para o Pokemon com ID {}".format(pokemon_id))
        time.sleep(10)

if __name__ == "__main__":
    main()