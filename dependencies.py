#Como cada rota, seja get, psot etc, dependem que eu crie uma sessão com o meu banco de dados para consulta, 
# sincronização e atualização, para poder otimizar o codigo e evitar repetições, vou criar uma função para abrir a sessão e fechá-la.
from fastapi import Depends, HTTPException
from models import db, user
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError

def initiate_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
#o unico problema é que não estou fechando a sessão, o que dependendo pode dar alguma interferência com outras sessões abertas em um sistema grande
#minha def irá "perceber" o meio, retornar o necessário, e já encontrar o fim. Substituindo o RETURN por YIELD
        yield session
    finally:
        session.close()

#Finally é extremamente importante para garantir que independente que dê erro, a sessão irá fechar

def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(initiate_session)):
    try:
        information_dic = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        user_id = int(information_dic.get("sub")) #int pq é um ID
    except JWTError:
        #usuario não tem autorização
        raise HTTPException (status_code= 401, detail= "Acesso negado. Verifique a validade do Token e tente novamente!")
    #extrair o id do usuario do token
    db_user =  session.query(user).filter(user.id==user_id).first()
    if not db_user:
        raise HTTPException (status_code= 401, detail= "Acesso inválido")
    return db_user

