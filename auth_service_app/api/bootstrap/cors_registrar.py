from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.dependencies import Config
from api.constants import constants


class CORSRegistrar:
    @staticmethod
    def register(app: FastAPI):
        """
        Registers CORS settings to the FastAPI application.

        This method adds the CORSMiddleware to the application with the
        specified settings for allowed origins, methods, headers, and
        credentials.
        """
        app.add_middleware(
            CORSMiddleware,
            allow_origins=Config().ALLOW_ORIGINS,
            allow_methods=constants.CORS_ALLOW_METHODS,
            allow_headers=constants.CORS_ALLOW_HEADERS,
            allow_credentials=Config().ALLOW_CREDENTIALS,
            max_age=Config().MAX_AGE,
        )
