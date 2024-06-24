from datetime import timedelta, datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '1e3bebac6b2b3dc3411ad4405f76773f'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class OAuth2PasswordRequestFormEmail(OAuth2PasswordRequestForm):
    def __init__(self, grant_type: str = Field(None, alias="grant_type"), email: str = Field(..., alias="username"), 
                 password: str = Field(..., alias="password"), scope: str = Field("", alias="scope"), 
                 client_id: Optional[str] = Field(None, alias="client_id"), 
                 client_secret: Optional[str] = Field(None, alias="client_secret")):
        
        super().__init__(grant_type=grant_type, username=email, password=password, 
                         scope=scope, client_id=client_id, client_secret=client_secret)

class CreateUserRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    acess_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user = User(
        email = create_user_request.email,
        password = bcrypt_context.hash(create_user_request.password)
    )

    db.add(create_user)
    db.commit()

    return { "message": 'User created successfuly!' }

@router.post("/token", response_model=Token)
async def login_for_acess_token(form_data: CreateUserRequest, db: db_dependency):
    user = authenticate_user(form_data.email, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    
    access_token_expires = timedelta(minutes=180)
    token = create_access_token(
        data={"sub": user.email, "id": user.id}, expires_delta=access_token_expires
    )
    return { 'acess_token': token, 'token_type': 'bearer' }

def authenticate_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": int(expire.timestamp())})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        user_id: int = payload.get('id')

        if email is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        
        return { 'email': email, 'id': user_id }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')