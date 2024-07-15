from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from database import SessionLocal, get_db
from schemas import ProductResponse, ProductUpdate, ProductCreate
from typing import List
from crud import (
    create_product, 
    get_products,
    get_product,
    delete_product,
    update_product
)

router = APIRouter()

### criar minha rota de buscar todos os itens
@router.get("/products/", response_model=List[ProductResponse])
def read_all_products(db: Session = Depends(get_db)):
    """
    Rota para buscar todos os itens
    """
    products = get_products(db)
    return products

### criar minha rota de buscar 1 item
@router.get("/products/{product_id}", response_model=ProductResponse)
def read_one_product(product_id: int, db: Session = Depends(get_db)):
    """
    Rota para buscar 1 item
    """
    db_product = get_product(db, product_id=product_id)
    if db_product is None: 
        raise HTTPException(status_code=4004, detail="voce está querendo buscar um produto inexistente")
    return db_product


### criar minha rota de adicionar um item
@router.post("/products/", response_model=ProductResponse)
def create_product_route(product: ProductCreate, db: Session = Depends(get_db)):
    """
    Rota para adicionar 1 item
    """
    return create_product(product=product, db=db)


### criar minha rota de deletar um item
@router.delete("/products/{product_id}", response_model=ProductResponse)
def delete_product_router(product_id: int, db: Session = Depends(get_db)):
    """
    Rota para deletar 1 item
    """
    db_product = delete_product(product_id=product_id, db=db)
    if db_product is None: 
        raise HTTPException(status_code=4004, detail="voce está querendo deletar um produto inexistente")
    return db_product

### criar minha rota de fazer update nos items
@router.put("/products/{product_id}", response_model=ProductResponse)
def atualizar_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)): 
    """
    Rota para realizar update dos items
    """
    db_product = update_product(db=db, product_id=product_id, product=product)
    if db_product is None: 
        raise HTTPException(status_code=4004, detail="voce está querendo realizar Update um produto inexistente")
    return db_product