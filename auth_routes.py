from fastapi import APIRouter, Depends, HTTPException
from models import user
from dependencies import initiate_session
#vou pegar meu bcrypt do main pra usar aqui
from main import bcrypt_context
from schemas import users_schemes, LoginSchemas
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def create_token(user_id):
    token = f"iahfuoi289739q{user_id}"
    return token


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
    db_user = session.query(user).filter(user.email==login_schema.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado. Tente novamente!")
    else:
        access_token = create_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
        #JWT Bearer
        headers = {"Access-Token" : "Bearer token"}
