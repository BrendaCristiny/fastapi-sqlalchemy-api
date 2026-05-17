from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import initiate_session
from schemas import OrderSchema
from models import order


order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
#Vamos fazer uma função do tipo: ASSINCRONO
async def orders():
    """Essa é a rota de pedidos padrão de nosso sistema."""
    return {"mensagem":"você acessou a rota de pedidos"}
    #usamos um dicionário porque a "restapi" se comunica por JSON, que é no formato de dicionário.


@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends (initiate_session)):
    new_order = order(user = order_schema.user)
    session.add(new_order)
    session.commit()
    return {"Mensagem": f"Pedido criado com sucesso! ID do pedido:{new_order.id}"}
