#Como cada rota, seja get, psot etc, dependem que eu crie uma sessão com o meu banco de dados para consulta, 
# sincronização e atualização, para poder otimizar o codigo e evitar repetições, vou criar uma função para abrir a sessão e fechá-la.

from models import db
from sqlalchemy.orm import sessionmaker

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

