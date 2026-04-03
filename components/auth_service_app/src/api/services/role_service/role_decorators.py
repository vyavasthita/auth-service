from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import (
    RoleAlreadyExistsException,
)


def is_new_role(func):
    """Decorator to ensure the role does not already exist before registration."""

    @wraps(func)
    async def wrapper(self, db_session: AsyncSession, role: str, *args, **kwargs):
        role_obj = await self._check_role(db_session, role)

        if role_obj is not None:
            raise RoleAlreadyExistsException(role=role)

        return await func(self, db_session, role, *args, **kwargs)

    return wrapper
