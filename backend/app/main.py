"""
RippleMap AI - Backend API Server
Production-grade FastAPI application with comprehensive API infrastructure
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from .config import settings
from .database import init_db, close_db
from .utils.logger import setup_logging
from .utils.exceptions import RippleMapException

# Setup logging
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Handles database initialization and cleanup.
    """
    # Startup
    logger.info("=" * 60)
    logger.info("Starting up RippleMap AI Backend...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise
    
    logger.info("=" * 60)
    yield
    
    # Shutdown
    logger.info("=" * 60)
    logger.info("Shutting down RippleMap AI Backend...")
    try:
        await close_db()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database: {str(e)}")
    logger.info("=" * 60)


# Initialize FastAPI app
app = FastAPI(
    title="RippleMap AI API",
    description="Enterprise-grade geospatial intelligence platform for analyzing road disruptions and their impact on essential services",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

# Compression middleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler for custom exceptions
@app.exception_handler(RippleMapException)
async def ripplemap_exception_handler(request, exc: RippleMapException):
    """Handle custom RippleMap exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message,
            "detail": exc.detail,
            "status_code": exc.status_code,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle unexpected exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
    )


# API Routes
from .api.v1.endpoints import (
    scenarios,
    routes,
    geospatial,
    analysis,
    admin,
    reports,
)

# Include API routers
api_v1_router_prefix = "/api/v1"

app.include_router(
    scenarios.router,
    prefix=f"{api_v1_router_prefix}/scenarios",
    tags=["Scenarios"],
)
app.include_router(
    routes.router,
    prefix=f"{api_v1_router_prefix}/routes",
    tags=["Routes"],
)
app.include_router(
    geospatial.router,
    prefix=f"{api_v1_router_prefix}/geospatial",
    tags=["Geospatial"],
)
app.include_router(
    analysis.router,
    prefix=f"{api_v1_router_prefix}/analysis",
    tags=["Analysis"],
)
app.include_router(
    admin.router,
    prefix=f"{api_v1_router_prefix}/admin",
    tags=["Admin"],
)
app.include_router(
    reports.router,
    prefix=f"{api_v1_router_prefix}/reports",
    tags=["Reports"],
)


# Health and status endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "success": True,
        "status": "healthy",
        "version": "1.0.0",
        "service": "RippleMap AI API",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information."""
    return {
        "success": True,
        "service": "RippleMap AI",
        "version": "1.0.0",
        "description": "Geospatial intelligence platform for disruption analysis",
        "documentation": "/api/docs",
        "endpoints": {
            "scenarios": "/api/v1/scenarios",
            "routes": "/api/v1/routes",
            "geospatial": "/api/v1/geospatial",
            "analysis": "/api/v1/analysis",
            "admin": "/api/v1/admin",
            "reports": "/api/v1/reports",
        },
    }


@app.get("/status", tags=["Status"])
async def status():
    """Detailed status endpoint."""
    return {
        "success": True,
        "status": "active",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "debug_mode": settings.DEBUG,
        "database_url": settings.DATABASE_URL.split("@")[1] if "@" in settings.DATABASE_URL else "***",
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize startup tasks."""
    logger.info("✓ RippleMap AI API started successfully")
    logger.info(f"✓ API Documentation available at http://localhost:{settings.PORT}/api/docs")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("✓ RippleMap AI API shutdown completed")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
