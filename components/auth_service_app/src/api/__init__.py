"""
FastAPI application initialization with modular OpenTelemetry observability setup.
"""

from fastapi import FastAPI

from src.api.bootstrap import AppFactory, AppInitializer

initializer = AppInitializer()
initializer.pre_initialization()

app: FastAPI = AppFactory.create_app()

initializer.post_initialization(app)
