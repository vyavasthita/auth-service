from fastapi import FastAPI
from api.dependencies import Config


class AppFactory:
    @staticmethod
    def create_app() -> FastAPI:
        return FastAPI(
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