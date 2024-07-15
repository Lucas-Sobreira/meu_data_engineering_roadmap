from sqlalchemy.orm import Session
from schemas import ProductUpdate, ProductCreate
from models import ProductModel

def get_products(db: Session):
    """
    Função que retorna todos os produtos [SELECT * FROM]
    """
    return db.query(ProductModel).all()

def get_product(db: Session, product_id: int):
    """
    Função que retorna o produto filtrado
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()

def create_product(db: Session, product: ProductCreate):
    """
    Função de criação de produto [Insert into]
    """
    # transformar minha view para ORM
    db_product = ProductModel(**product.model_dump())

    # adicionar na tabela 
    db.add(db_product)

    # commitar na minha tabela 
    db.commit()

    # fazer o refresh do banco de dados
    db.refresh(db_product)

    # retornar pro usuario o item criado
    return db_product

def delete_product(db: Session, product_id: int):
    """
    Função que deleta o produto desejado
    """
    # Fitra o produto à ser deletado
    db_product =  db.query(ProductModel).filter(ProductModel.id == product_id).first()

    # Deleta o produto
    db.delete(db_product)
    
    # Commita a deleção do produto
    db.commit()

    # retornar pro usuario o item criado
    return db_product

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    if db_product is None: 
        return None

    if product.nome is not None: 
        db_product.nome = product.nome
    if product.descricao is not None: 
        db_product.descricao = product.descricao
    if product.preco is not None: 
        db_product.preco = product.preco
    if product.categoria is not None: 
        db_product.categoria = product.categoria
    if product.email_fornecedor is not None: 
        db_product.email_fornecedor = product.email_fornecedor
    db.commit()
    db.refresh(db_product)
    return db_product