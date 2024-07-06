from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine
from sqlalchemy import text

# Transforma em um banco de dados
class HERO(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

engine = create_engine("sqlite:///database.db", echo=True)

SQLModel.metadata.create_all(engine)

hero_1 = HERO(name="Deadpond", secret_name="Dive Wilson")
hero_2 = HERO(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = HERO(name="Rust-Man", secret_name="Tommy Sharp", age=48)

with Session(engine) as session: 
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()