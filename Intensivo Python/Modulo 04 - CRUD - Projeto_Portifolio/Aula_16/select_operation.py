from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy import text

# Supondo que o banco de dados seja SQLite e esteja no arquivo 'database.db'
engine = create_engine("sqlite:///database.db")

# Criando a sessão
with Session(engine) as session: 
    # Sua consulta SQL
    statement= text("SELECT * FROM hero;")

    # Executando a consulta 
    results = session.exec(statement)

    # Fetch dos resultados 
    heroes = results.fetchall()

    for hero in heroes: 
        print(hero)