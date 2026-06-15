from fastapi import FastAPI
#para criptografar as senhas:
from passlib.context import CryptContext
#pra carregar as variaveis de ambiente dentro do meu arquivo .env
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
#Ler variáveis do .env
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) #int pq é número (a expiração)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login-form")

#instância da classe:
app = FastAPI()

#como eu criei arquivos individuais para organizar as rotas, vou importá-los:
from auth_routes import auth_router
from order_routes import order_router

#vou pedir para meu arquivo atual incluir minhas rotas aqui:
app.include_router(auth_router)
app.include_router(order_router)
