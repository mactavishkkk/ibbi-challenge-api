from fastapi import FastAPI
from .routers import users, categories, products
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def helloworldd():
    return {"message": "Hello, world!"}

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(products.router, prefix="/products", tags=["products"])
