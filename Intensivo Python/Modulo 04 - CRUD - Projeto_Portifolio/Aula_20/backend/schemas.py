from pydantic import BaseModel, PositiveFloat, EmailStr, validator
from enum import Enum
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel): 
    nome: str
    descricao: str
    preco: PositiveFloat
    categoria: str
    email_fornecedor: EmailStr

# Select 
class ProductResponse(ProductBase): 
    id: int
    data_criacao: datetime
    
    class Config: 
        from_attributes = True

# Insert
class ProductCreate(ProductBase):
    pass

# Update
class ProductUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[PositiveFloat] = None
    categoria: Optional[str] = None
    email_fornecedor: Optional[str] = None