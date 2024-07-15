from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class ProductModel(Base): 
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    preco = Column(Float)
    categoria = Column(String)
    email_fornecedor = Column(String)
    data_criacao = Column(DateTime(timezone=True), default=func.now())