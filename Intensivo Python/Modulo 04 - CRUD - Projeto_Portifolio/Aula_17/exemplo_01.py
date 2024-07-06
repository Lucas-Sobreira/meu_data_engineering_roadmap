from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# ## URI = "postgresql_pyodbc://dbuser:kx%40jj5%2Fg@pghost10/appdb"
# ## dialect+driver://username:password@host:port/database

# # Conectar ao SQLite em memória 
engine = create_engine('sqlite:///meubanco.db', echo=True)
print("Conexão com SQLite estabelecida")

Base = declarative_base()

# Criando a Classe da Tabela
class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    idade = Column(Integer)

# Criando Database
Base.metadata.create_all(engine)

# Criando Sessão e Inserindo os dados na Tabela
Session = sessionmaker(bind=engine)

with Session() as session:
    novo_usuario = Usuario(nome='Mario', idade=23)
    session.add(novo_usuario)
    session.commit()