from datetime import datetime
from sqlalchemy.orm import declarative_base


SQLAlchemyBase = declarative_base()

class Base:
    def __init__(self):
        self._id: int

    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id: int) -> None:
        self._id = id