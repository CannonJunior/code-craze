"""
Main FastAPI application server for Code Craze Study Guide.

This is the entry point for the backend API server running on port 8989.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn

from backend.config.settings import settings
from backend.database.db import init_db
from backend.api import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup: Initialize database
    print("🚀 Starting Code Craze Academy...")
    print(f"📊 Initializing database at {settings.database_url}")
    init_db()
    print("✅ Database initialized")

    yield

    # Shutdown
    print("👋 Shutting down Code Craze Academy...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Interactive study guide for Science Olympiad Code Craze event",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(routes.router, prefix="/api")

# Mount static files (frontend)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Health status and application info.
    """
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "port": settings.port,
    }


def main():
    """
    Run the FastAPI application with uvicorn.

    This is the entry point when running with: uv run server.py
    """
    print(f"🎯 {settings.app_name} v{settings.app_version}")
    print(f"🌐 Server starting on port {settings.port}")
    print(f"🔗 Open http://localhost:{settings.port} in your browser")
    print(f"📚 API docs available at http://localhost:{settings.port}/docs")

    uvicorn.run(
        "backend.server:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.debug,
        log_level="info",
    )


if __name__ == "__main__":
    main()
