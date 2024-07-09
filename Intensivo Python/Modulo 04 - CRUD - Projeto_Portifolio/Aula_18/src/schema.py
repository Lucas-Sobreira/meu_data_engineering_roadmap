from pydantic import BaseModel

class PokemonSchema(BaseModel): # Contrato de Dados, Schema de Dados
    name: str
    type: str

    class Config: 
        # orm_mode = True
        from_attributes = True