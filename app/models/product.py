from sqlalchemy import Column, Integer, orm, CHAR, VARCHAR
from app.models.base import Base


class Product(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=True)
    lev30 = Column(CHAR(36), nullable=False)
    lev20 = Column(CHAR(36), nullable=False)
    lev17 = Column(CHAR(36), nullable=False)
    lev15 = Column(CHAR(36), nullable=False)
    lev10 = Column(CHAR(36), nullable=False)

    # pubdate = Column(String(20))
    # isbn = Column(String(15), nullable=False, unique=True)
    # summary = Column(String(1000))
    # image = Column(String(50))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'name', 'lev30', 'lev20',
                       'lev17', 'lev15', 'lev10']
