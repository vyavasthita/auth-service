from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.utils import KeyManager

jwks_router = APIRouter(
    prefix="/token",
    tags=["JWKS"],
)


@jwks_router.get("/.well-known/jwks.json")
async def get_jwks() -> JSONResponse:
    """Serve the public key set for token signature verification."""
    return JSONResponse(
        content=KeyManager().get_jwks(),
        headers={"Cache-Control": "public, max-age=3600"},
    )
