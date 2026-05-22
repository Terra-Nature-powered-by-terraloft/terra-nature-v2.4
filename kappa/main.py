"""
Terra Nature Assistent Kappa
FastAPI Expert Engine Entry Point

Lokaler, projektgebundener Expertenassistent für Terra Nature powered by Terraloft
"""

import sys
from pathlib import Path

# Add kappa to path for imports
KAPPA_DIR = Path(__file__).parent
sys.path.insert(0, str(KAPPA_DIR))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import json

from .config import config
from .utils.logging import logger, setup_logging
from .api.routes import router as kappa_router

# Initialize logging
setup_logging()

logger.info(
    "kappa_startup",
    environment=config.environment,
    debug=config.debug,
    mock_mode=config.mock_mode,
    port=config.port,
    host=config.host,
)

# === LIFECYCLE EVENTS ===

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("kappa_startup_complete")
    yield
    logger.info("kappa_shutdown")

# === FASTAPI APP ===

app = FastAPI(
    title="Terra Nature Assistent Kappa",
    description="Lokaler projektgebundener Expertenassistent für Terra Nature powered by Terraloft",
    version="0.1.0-phase1",
    lifespan=lifespan,
)

# === MIDDLEWARE ===

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests"""
    logger.info(
        "http_request",
        method=request.method,
        path=request.url.path,
        client=request.client.host if request.client else "unknown"
    )
    response = await call_next(request)
    logger.info(
        "http_response",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code
    )
    return response

# === ROUTES ===

# Include Kappa router
app.include_router(kappa_router)

# === ERROR HANDLERS ===

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error("unhandled_exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "code": "INTERNAL_ERROR",
            "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z"
        }
    )

# === ROOT ENDPOINT ===

@app.get("/")
async def root():
    """Root endpoint - API documentation"""
    return {
        "name": "Terra Nature Assistent Kappa",
        "version": "0.1.0-phase1",
        "status": "operational",
        "docs": "/docs",
        "environment": config.environment,
        "mock_mode": config.mock_mode,
    }

# === MAIN ===

if __name__ == "__main__":
    import uvicorn

    logger.info(
        "starting_uvicorn",
        host=config.host,
        port=config.port,
        debug=config.debug
    )

    uvicorn.run(
        "main:app",
        host=config.host,
        port=config.port,
        reload=config.debug,
        log_level="debug" if config.debug else "info",
    )
