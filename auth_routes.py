from fastapi import APIRouter, Depends, HTTPException
from models import user
from dependencies import initiate_session, verify_token
#vou pegar meu bcrypt do main pra usar aqui
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import users_schemes, LoginSchemas
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(user_id, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):

    expiration_date = (
        datetime.now(timezone.utc)
        + token_duration
    )

    information_dic = {
        "sub": str(user_id),
        "exp": expiration_date
    }

    encoded_jwt = jwt.encode(
        information_dic,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt



def authenticate_user(email,password, session):
    db_user = session.query(user).filter(user.email==email).first()
    if not db_user:
        return False
    elif not bcrypt_context.verify(password, db_user.password):
        return False
    return db_user 


@auth_router.get("/")
async def home():
    """Essa é a rota de autenticação padrão de nosso sistema."""
    return {"mensagem":"Você chegou a rota de autorização.", "autenticado":False}

#POST por que estou "mandando informações no sistema", pois o site vai receber infomações e mandar elas
@auth_router.post("/create_account")
#preciso criar parametros e especifica-los para que seja possível o acesso. 
async def create_account(UsersSchemes:users_schemes, session:Session=Depends(initiate_session)):
    #para que seja possível permitir o acesso é necessario criar uma sessão para fazer uma busca no meu banco de dados, acima a sessão foi feita "dependendo" de uma função que abre a minha sessão
    #agora com a sessão já iniciada e vou buscar (query) dentro do meu banco, oq eu preciso:
    existing_user = session.query(user).filter(user.email==UsersSchemes.email).first()
    if existing_user:
        #return {"mensagem": "Já existe um usuário com ess e-mail!"} mensagem genérica
        raise HTTPException(status_code=400, detail="E-mail informado já cadastrado no sistema. Tente novamente!") #mensagem personalizada com exception
    else:
        encrypted_password = bcrypt_context.hash(UsersSchemes.password)
        #Como estruturei os requisitos em "schemes" vou chamá-lo junto:
        new_user = user(UsersSchemes.name, UsersSchemes.email, encrypted_password, UsersSchemes.active, UsersSchemes.admin)
        #adicionar e dar o commit:
        session.add(new_user)
        session.commit()
        return {"mensagem": f"Usuário cadastrado com sucesso, no E-mail: {UsersSchemes.email}"}
    

#Estritura do login: email e senha -> toker JWT (Json Web Token)

@auth_router.post("/login")
async def login(login_schema: LoginSchemas, session: Session = Depends (initiate_session)):
    db_user = authenticate_user(login_schema.email, login_schema.password, session)
    if not db_user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado, ou credenciais inválidas. Tente novamente!")
    else:
        access_token = create_token(db_user.id)
        refresh_token = create_token(db_user.id, token_duration=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    
#criar um novo end point de login para o botão "authorize" no canto superior direito funcionar
@auth_router.post("/login-form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends (), session: Session = Depends (initiate_session)):
    db_user = authenticate_user(form_data.username, form_data.password, session)
    if not db_user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado, ou credenciais inválidas. Tente novamente!")
    else:
        access_token = create_token(db_user.id)
        refresh_token = create_token(db_user.id, token_duration=timedelta(days=7))
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
        
@auth_router.get("/refresh")
async def use_refresh_token(db_user: user =  Depends (verify_token)):
    #verificar o token
    access_token = create_token(db_user.id)
    return {
            "access_token": access_token,
            "token_type": "Bearer"
        }