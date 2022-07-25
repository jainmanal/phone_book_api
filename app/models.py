from sqlalchemy import BigInteger, Column, Integer, String

from .db import Base
    
class User_detail(Base):
    __tablename__ = "user details"
    
    id = Column(Integer, primary_key=True,index=True)
    first_name = Column(String(80), nullable=False, index=True)
    last_name = Column(String(80), nullable=False, index=True)
    phone = Column(BigInteger(), nullable=False, unique=True)
    def __repr__(self):
        return 'ItemModel(first_name=%s, last_name=%s,phone=%s)' % (self.first_name, self.last_name, self.phone)
