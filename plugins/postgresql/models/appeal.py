from . import Base
from sqlalchemy import Column
from sqlalchemy import BIGINT, INTEGER, TEXT, BOOLEAN
from sqlalchemy.orm import Mapped


class Appeal(Base): # Таблица "Обращения"
    __tablename__ = 'appeal'
    
    msg_id:Mapped[INTEGER] = Column(INTEGER, unique=True, index=True,primary_key=True)
    tg_id:Mapped[BIGINT] = Column(BIGINT, index=True)
    operands:Mapped[TEXT] = Column(TEXT)
    status:Mapped[BOOLEAN] = Column(BOOLEAN,default=True)
    result:Mapped[TEXT] = Column(TEXT)
    photo:Mapped[TEXT] = Column(TEXT, default=None)
    point:Mapped[INTEGER] = Column(INTEGER)