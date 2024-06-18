from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import schemas, database

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
import seed

engine = create_engine(database.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

def seed_users(db: Session):
    user = schemas.UserCreate(email="ionet@example.com", password="password")
    user1 = schemas.UserCreate(email="maraiza@example.com", password="password")
    user2 = schemas.UserCreate(email="greyce@example.com", password="password")

    db_user = schemas.User(**user.dict())
    db_user1 = schemas.User(**user1.dict())
    db_user2 = schemas.User(**user2.dict())

    db.add(db_user)
    db.add(db_user1)
    db.add(db_user2)

    db.commit()

def seed_categories(db: Session):
    category = schemas.CategoryCreate(name="Eletronicos", description="Dispositivos eletrônicos e gadgets")
    category1 = schemas.CategoryCreate(name="Roupas", description="Vestuário e itens de moda")
    category2 = schemas.CategoryCreate(name="Objetos", description="Objetos e utensílios no geral")

    db_category = schemas.Category(**category.dict())
    db_category1 = schemas.Category(**category1.dict())
    db_category2 = schemas.Category(**category2.dict())

    db.add(db_category)
    db.add(db_category1)
    db.add(db_category2)

    db.commit()

def seed_products(db: Session):
    product = schemas.ProductCreate(
        name="Smartphone",
        description="Último modelo de smartphone",
        value=999.99,
        dolarValue=200.0,
        image="smartphone.jpg",
        quantity=10,
        status="green",
        category_id=1 
    )
    product1 = schemas.ProductCreate(
        name="T-shirt",
        description="Camiseta casual de algodão",
        value=29.99,
        dolarValue=6.0,
        image="tshirt.jpg",
        quantity=0,
        status="red",
        category_id=2
    )
    product2 = schemas.ProductCreate(
        name="Knife",
        description="Faca de aço inox",
        value=9.92,
        dolarValue=2.0,
        image="knife.jpg",
        quantity=3,
        status="red",
        category_id=3
    )

    db_product = schemas.Product(**product.dict())
    db_product1 = schemas.Product(**product1.dict())
    db_product2 = schemas.Product(**product2.dict())

    db.add(db_product)
    db.add(db_product1)
    db.add(db_product2)

    db.commit()

def seed_all(db: Session):
    seed_users(db)
    seed_categories(db)
    seed_products(db)

try:
    seed.seed_all(db)
    print("Dados adicionados com sucesso!")
except Exception as e:
    print(f"Ocorreu um erro ao adicionar dados de seed: {str(e)}")
finally:
    db.close()
