from datetime import datetime

from sqlalchemy import ForeignKey, LargeBinary, func
from sqlalchemy.orm import Mapped, mapped_column

from src.api.models.base import Base


class UserRole(Base):
    __tablename__ = "users_roles"

    user_id: Mapped[bytes] = mapped_column(LargeBinary(16), ForeignKey("users.user_id"), primary_key=True)
    role_id: Mapped[bytes] = mapped_column(LargeBinary(16), ForeignKey("roles.role_id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
