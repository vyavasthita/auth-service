from datetime import datetime

from sqlalchemy import LargeBinary, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.models.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[bytes] = mapped_column(LargeBinary(16), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user", uselist=False)  # noqa: F821
    sessions: Mapped[list["UserSession"]] = relationship("UserSession", back_populates="user")  # noqa: F821
