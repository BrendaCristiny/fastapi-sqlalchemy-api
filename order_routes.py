from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import initiate_session, verify_token
from schemas import OrderSchema
from models import order, user

#Qualquer dependencia aqui, irá aplicar para todas 
order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)])

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

# colchetes para passar na rota como parâmetro
@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(initiate_session), db_user: user = Depends(verify_token)):
    order = session.query(order).filter(order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=400,
            detail="Pedido não encontrado, ou não existente."
        )

    # Se não for admin E não for dono do pedido
    if not db_user.admin and db_user.id != order.user:
        raise HTTPException(
            status_code=401,
            detail="Você não tem permissão para performar essa ação."
        )
    order.status = "cancelled"
    session.commit()  # salvar alterações

    return {
        "mensagem": f"Pedido número:{order.id} cancelado com sucesso!",
        "pedido": order
    }