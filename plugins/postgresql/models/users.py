from sqlalchemy.orm import DeclarativeBase
from . import Base
from sqlalchemy import Column
from sqlalchemy import BIGINT, INTEGER, TEXT, BOOLEAN
from sqlalchemy.orm import Mapped


class Users(Base): # Таблица "Пользователи"
    __tablename__ = 'users'
    
    tg_id:Mapped[BIGINT] = Column(BIGINT, primary_key=True, nullable=False)
    num_try:Mapped[INTEGER] = Column(INTEGER,default=0)
    tg_link:Mapped[TEXT] = Column(TEXT, default=None)
    status:Mapped[BOOLEAN] = Column(BOOLEAN,default=True)
    lang:Mapped[TEXT] = Column(TEXT)