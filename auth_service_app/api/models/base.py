from datetime import datetime
from sqlalchemy.orm import declarative_base


SQLAlchemyBase = declarative_base()

class Base:
    def __init__(self):
        """
        Initialize the base model with an ID attribute.
        """
        self._id: int

    @property
    def id(self) -> int:
        """
        Get the ID of the model instance.
        Returns:
            int: The ID value.
        """
        return self._id
    
    @id.setter
    def id(self, id: int) -> None:
        """
        Set the ID of the model instance.
        Args:
            id (int): The new ID value.
        """
        self._id = id