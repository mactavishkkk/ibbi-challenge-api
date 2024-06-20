from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
import routers.users as ru, routers.categories as rc, routers.products as rp, auth, database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:4201",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def helloworldd():
    return {"message": "Hello, world!"}

app.include_router(auth.router);
app.include_router(ru.router, prefix="/users", tags=["users"])
app.include_router(rc.router, prefix="/categories", tags=["categories"])
app.include_router(rp.router, prefix="/products", tags=["products"])
