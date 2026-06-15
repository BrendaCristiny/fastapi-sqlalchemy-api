from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

#cria a conexão do banco
db= create_engine("sqlite:///data.db")

#cria a base do banco 
Base = declarative_base()

#criar as classes/tabela do banco

#USUARIO
class user(Base):
    __tablename__= "users"
#À esquerda é o nome da classe "id", à direita tem o nome da coluna entre parentes, igual vai estar do seu banco de dados
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column ("name", String)
    email = Column ("email", String, nullable= False)
    password = Column ("password", String)
    active = Column ("active", Boolean)
    admin =  Column ("admin", Boolean, default=False)

#Sempre que eu for criar um usuario eu tenho que passar o que? bote entre parenteses neste comando:
    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin


#PEDIDO
class order(Base):
    __tablename__ = "orders"

    #definindo status com tupla (a função que pede) para que as opções sejam limitadas a essas:
    #order_status= (
     #   ("pending", "pending"),
      #  ("cancelled", "cancelled"),
       # ("Finished", "finished")
    #)

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column ("status", String) #pendente, cancelado, finalizado
    user = Column(Integer, ForeignKey("users.id"))#o id da outra tabela, para ambos mostrarem o meu usuario
    price = Column ("price", Float)
    #Vou conectar ambas as tabelas sem necessariamente criar uma dependencia
    items = relationship("item_ordered", cascade="all, delete") #cascade = quando eu deletar um pedido especifico ele vai cascadear/sincronizar esse processo para todos relacionados

    def __init__(self, user, status="pending", price=0):
        self.user = user
        self.price = price
        #preciso definir que só é possível 3 opções (pendente, cancelado, finalizado)
        self.status = status

    def calculate_price(self):
        self.price = sum(
            item.unit_price * item.amount
            for item in self.items
        )

#ITENS PEDIDO
class item_ordered(Base):
    __tablename__= "items_ordered"

    id = Column ("id", Integer, primary_key=True, autoincrement=True)
    amount = Column ("amount", Integer)
    flavor = Column ("flavor", String)
    size = Column ("size", String)
    unit_price = Column ("unit_price", Float)
    order = Column(Integer, ForeignKey("orders.id"))
    #você pode fazer varios "status_pedido" para tamanho, pedido, sabor, e etc. mas eui particularmente não vou fazer, vou manter simples por enquanto

    def __init__(self, amount, flavor, size, unit_price, order):
        self.amount = amount
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order = order

        
#executar a criação dos metadados do banco
Base.metadata.create_all(bind=db)

