from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

POSTGRES_DATABASE_URL = "postgresql://user:password@postgres/mydatabase"

engine = create_engine(POSTGRES_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(): 
    db = SessionLocal()
    try: 
        yield db # retorna a Sessão Instanciada
    finally: 
        db.close()