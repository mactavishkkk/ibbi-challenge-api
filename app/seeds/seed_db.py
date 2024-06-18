from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import database

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
import seed

engine = create_engine(database.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()

try:
    seed.seed_all(db)
    print("Dados adicionados com sucesso!")
except Exception as e:
    print(f"Ocorreu um erro ao adicionar dados de seed: {str(e)}")
finally:
    db.close()
