from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import models, utils

def seed_users(db: Session):
    hashed_password = utils.get_password_hash("password");

    user = models.User(email="ionet@example.com", password=hashed_password)
    user1 = models.User(email="maraiza@example.com", password=hashed_password)
    user2 = models.User(email="greyce@example.com", password=hashed_password)

    db.add(user)
    db.add(user1)
    db.add(user2)

    db.commit()

def seed_categories(db: Session):
    category = models.Category(name="Eletronicos", description="Dispositivos eletrônicos e gadgets")
    category1 = models.Category(name="Roupas", description="Vestuário e itens de moda")
    category2 = models.Category(name="Objetos", description="Objetos e utensílios no geral")

    db.add(category)
    db.add(category1)
    db.add(category2)

    db.commit()

def seed_products(db: Session):
    product = models.Product(
        name="Smartphone",
        description="Último modelo de smartphone",
        value=999.99,
        dolarValue=200.0,
        image="smartphone.jpg",
        quantity=10,
        status="green",
        category_id=1 
    )
    product1 = models.Product(
        name="T-shirt",
        description="Camiseta casual de algodão",
        value=29.99,
        dolarValue=6.0,
        image="tshirt.jpg",
        quantity=0,
        status="red",
        category_id=2
    )
    product2 = models.Product(
        name="Knife",
        description="Faca de aço inox",
        value=9.92,
        dolarValue=2.0,
        image="knife.jpg",
        quantity=3,
        status="red",
        category_id=3
    )

    db.add(product)
    db.add(product1)
    db.add(product2)

    db.commit()

def seed_all(db: Session):
    seed_users(db)
    seed_categories(db)
    seed_products(db)
