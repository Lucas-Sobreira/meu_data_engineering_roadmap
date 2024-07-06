from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

# Criando as Classes
class Fornecedor(Base):
    __tablename__ = 'fornecedores'    
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    telefone = Column(String(20))
    email = Column(String(50))
    endereco = Column(String(100))

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(200))
    preco = Column(Float)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'))
    
    # Estabelece a relação entre Produto e Fornecedor
    fornecedor = relationship("Fornecedor")

# Definindo as funções que contém os dados e o Commit
def commit_changes(session, tabela): 
    session.add_all(tabela)
    session.commit()

def insert_fornecedores(session) -> None: 
    try: 
        with session: # Usando a sessão corretamente com o gerenciador de contexto
            fornecedores = [
                Fornecedor(nome="Fornecedor A", telefone="12345678", email="contato@a.com", endereco="Endereço A"),
                Fornecedor(nome="Fornecedor B", telefone="87654321", email="contato@b.com", endereco="Endereço B"),
                Fornecedor(nome="Fornecedor C", telefone="12348765", email="contato@c.com", endereco="Endereço C"),
                Fornecedor(nome="Fornecedor D", telefone="56781234", email="contato@d.com", endereco="Endereço D"),
                Fornecedor(nome="Fornecedor E", telefone="43217865", email="contato@e.com", endereco="Endereço E")
            ]

            commit_changes(session, fornecedores)
    except SQLAlchemyError as e: # Captuando exceções do SQLAlchemy
        print(f"Erro ao inserir fornecedores {e}")

def insert_produtos(session) -> None: 
    try: 
        with session: # Usando a sessão corretamente com o gerenciador de contexto
            produtos = [
                Produto(nome="Produto 1", descricao="Descrição do Produto 1", preco=100, fornecedor_id=1),
                Produto(nome="Produto 2", descricao="Descrição do Produto 2", preco=200, fornecedor_id=2),
                Produto(nome="Produto 3", descricao="Descrição do Produto 3", preco=300, fornecedor_id=3),
                Produto(nome="Produto 4", descricao="Descrição do Produto 4", preco=400, fornecedor_id=4),
                Produto(nome="Produto 5", descricao="Descrição do Produto 5", preco=500, fornecedor_id=5)
            ]

            commit_changes(session, produtos)
    except SQLAlchemyError as e: # Captuando exceções do SQLAlchemy
        print(f"Erro ao inserir fornecedores {e}")


# Criando o Banco de Dados e as Tabelas
engine = create_engine('sqlite:///desafio.db', echo=True)
Base.metadata.create_all(engine)

# Criando a sessão
Session = sessionmaker(bind=engine)
session = Session()

# Inserindo os dados nas Tabelas 
insert_fornecedores(session)
insert_produtos(session)

# Visualizando os dados Inseridos
for produto in session.query(Produto).all():
    print(f"Produto: {produto.nome}, Fornecedor: {produto.fornecedor.nome}")