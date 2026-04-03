from datetime import datetime

from sqlalchemy import ForeignKey, LargeBinary, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.models.base import Base


class UserProfile(Base):
    __tablename__ = "users_profiles"

    user_profile_id: Mapped[bytes] = mapped_column(LargeBinary(16), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    user_id: Mapped[bytes] = mapped_column(LargeBinary(16), ForeignKey("users.user_id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="profile")  # noqa: F821
