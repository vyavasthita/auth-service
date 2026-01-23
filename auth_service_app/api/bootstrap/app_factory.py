from fastapi import FastAPI
from fastapi import FastAPI
from api.dependencies import Config
from api.repositories.db import BaseDB

class AppFactory:
    @staticmethod
    def create_app() -> FastAPI:
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
            root_path="/auth-service",
            docs_url=Config().OPEN_API_DOCS_URL if Config().ENABLE_SWAGGER_UI else None,
            redoc_url=Config().OPEN_API_RE_DOC_URL if Config().ENABLE_SWAGGER_UI else None,
        )

        # Register DB shutdown event handler directly here
        @app.on_event("shutdown")
        async def _shutdown_db_engine():
            await BaseDB().dispose_engine()

        return app