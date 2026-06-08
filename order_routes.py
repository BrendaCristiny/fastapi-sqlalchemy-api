from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import initiate_session, verify_token
from schemas import OrderSchema, ItemOrderSchema
from models import order, user, item_ordered

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

@order_router.get("/list")
async def list_orders(session: Session = Depends(initiate_session), db_user: user = Depends(verify_token)):
    if not db_user.admin:
        raise HTTPException(
            status_code=401,
            detail="Você não tem permissão para fazer essa operação."
        )
    else:
        orders = session.query(order).all() #Estamos usando ALL por ser um sistema pequeno, geralmente sistemas maiores o interessante é especificar o ID ou utilizar outros meios para otimização de tempo
        return {
            "Pedidos" : orders
        }
    
@order_router.post("/order/add-item/{order_id}")
async def add_order(order_id: int, item_order_schema : ItemOrderSchema, session: Session = Depends(initiate_session), db_user: user = Depends(verify_token)):
    Order = session.query(order).filter(order.id==order_id).first()
    if not Order:
        raise HTTPException(status_code=400, detail="Pedido não existente")
    if not db_user.admin and db_user.id != Order.user:
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa operação.")
    Item_Ordered = item_ordered(item_order_schema.amount, item_order_schema.flavor, item_order_schema.size, item_order_schema.unit_price, order_id)
    session.add(Item_Ordered)
    session.commit()
    Order.calculate_price()
    session.commit()
    return {
        "mensagem" : "Item criado com sucesso",
        "item_id" : Item_Ordered.id,
        "Preco_pedido": Order.price
    }