from sqlalchemy import String, Column, LargeBinary

from api.models import SQLAlchemyBase

    
class User(SQLAlchemyBase):
    __tablename__ = "users"

    id = Column(LargeBinary, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    phone_number = Column(String)
