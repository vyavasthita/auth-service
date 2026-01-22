"""
FastAPI application initialization with modular OpenTelemetry observability setup.

This file wires together logging, tracing, and metrics instrumentation for the API,
using a dedicated AppInitializer class for maintainability and clarity.
All configuration is loaded from the central Config class for future Kubernetes compatibility.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api.bootstrap import AppFactory, AppInitializer

initializer = AppInitializer()

# Pre-initialization steps (placeholder for future use)
initializer.pre_initialization()


app: FastAPI = AppFactory.create_app()

# --- Exception Handlers ---

# Exception handlers are now registered in post_initialization


# Post-initialization steps: wire up OpenTelemetry and routers
initializer.post_initialization(app)