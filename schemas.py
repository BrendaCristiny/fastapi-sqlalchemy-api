#força o python a pedir certos dados; str, int, e etc. para garantir a integridade do sistema.

from pydantic import BaseModel
#para que alguns parâmtros possam ser opcionais
from typing import Optional

class users_schemes(BaseModel):
    name: str
    email: str
    password: str
    active: Optional [bool] = True
    admin: Optional [bool] = False

    #Para que ele seja interpretado como ORM, ou seja, uma classe a ser transformada em sql, nosso usuario do modelo/models
    class Config:
        from_attributes= True

class OrderSchema(BaseModel):
    user: int
    class Config:
        from_attributes= True

class LoginSchemas(BaseModel):
    email: str
    password:str

    class Config:
        from_attributes = True

class ItemOrderSchema(BaseModel):
    amount : int
    flavor : str
    size : str
    unit_price : float
    '''order_id = int'''#n está aqui porque está já sendo exigido em nossa rota

    class Config:
        from_attributes = True