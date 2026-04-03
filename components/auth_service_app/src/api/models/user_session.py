import enum
from datetime import datetime

from sqlalchemy import Enum, ForeignKey, LargeBinary, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.models.base import Base


class SessionStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"


class UserSession(Base):
    __tablename__ = "users_sessions"

    user_session_id: Mapped[bytes] = mapped_column(LargeBinary(16), primary_key=True)
    token: Mapped[str] = mapped_column(Text, nullable=False)
    jti: Mapped[str] = mapped_column(String(36), nullable=False, unique=True)
    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus, native_enum=True), nullable=False, default=SessionStatus.ACTIVE
    )
    user_id: Mapped[bytes] = mapped_column(LargeBinary(16), ForeignKey("users.user_id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    modified_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship("User", back_populates="sessions")  # noqa: F821
