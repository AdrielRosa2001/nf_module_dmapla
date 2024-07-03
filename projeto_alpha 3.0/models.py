from sqlalchemy import Column, Integer, String
from databse import Base

class Pedido(Base):
    __tablename__ = 'notas_a_emitir'
    id = Column(Integer, autoincrement=True, primary_key=True)
    numero_pedido = Column(String(125), unique=False)
    valor = Column(String(125), unique=False)

    def __init__(self, numero_pedido=None):
        self.numero_pedido = numero_pedido
    
    def as_dict(self):
        return {"id": self.id, "numero_pedido": self.numero_pedido}

class Pedido_Emitido(Base):
    __tablename__ = 'notas_ok'
    id = Column(Integer, autoincrement=True, primary_key=True)
    numero_pedido = Column(String(125), unique=False)

    def __init__(self, numero_pedido=None):
        self.numero_pedido = numero_pedido

    
    def as_dict(self):
        return {"id": self.id, "numero_pedido": self.numero_pedido}


class Pedido_Falho(Base):
    __tablename__ = 'notas_falhas'
    id = Column(Integer, autoincrement=True, primary_key=True)
    numero_pedido = Column(String(125), unique=False)

    def __init__(self, numero_pedido=None, ):
        self.numero_pedido = numero_pedido
    
    def as_dict(self):
        return {"id": self.id, "numero_pedido": self.numero_pedido}