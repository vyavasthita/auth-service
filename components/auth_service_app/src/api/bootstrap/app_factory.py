from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.dependencies.config_dependency import Config
from src.api.repos.db import DatabaseEngine


class AppFactory:
    @staticmethod
    def create_app() -> FastAPI:
        """Create and configure the FastAPI application instance."""

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            await DatabaseEngine().dispose_engine()

        app = FastAPI(
            title="Auth Service",
            summary="Authentication and Authorisation service",
            description=(
                "* Github: [Dilip Sharma](https://github.com/vyavasthita)\n"
                "* LinkedIn: [Dilip Sharma](https://www.linkedin.com/in/diliplakshya/)\n"
            ),
            version="0.0.1",
            contact={
                "Name": "Dilip Sharma",
            },
            root_path=f"/{Config().SERVICE_NAME}",
            docs_url=Config().OPEN_API_DOCS_URL if Config().ENABLE_SWAGGER_UI else None,
            redoc_url=Config().OPEN_API_RE_DOC_URL if Config().ENABLE_SWAGGER_UI else None,
            lifespan=lifespan,
        )

        return app
