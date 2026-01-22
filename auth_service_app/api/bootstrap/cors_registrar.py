from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.dependencies import Config
from api.constants import constants


class CORSRegistrar:
    @staticmethod
    def register(app: FastAPI):
        app.add_middleware(
            CORSMiddleware,
            allow_origins=Config().ALLOW_ORIGINS,
            allow_methods=constants.CORS_ALLOW_METHODS,
            allow_headers=constants.CORS_ALLOW_HEADERS,
            allow_credentials=Config().ALLOW_CREDENTIALS,
            max_age=Config().MAX_AGE,
        )
