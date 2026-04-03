from datetime import datetime

from sqlalchemy import LargeBinary, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.api.models.base import Base


class Role(Base):
    __tablename__ = "roles"

    role_id: Mapped[bytes] = mapped_column(LargeBinary(16), primary_key=True)
    role_name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())