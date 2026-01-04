from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.utils.security import add_security_headers


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title="Todo API",
        description="A full-stack todo web application with user authentication and task management capabilities",
        version="0.1.0",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
    )

    # Add security headers
    app = add_security_headers(app)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(auth_router, prefix=settings.api_prefix, tags=["auth"])
    app.include_router(tasks_router, prefix=settings.api_prefix, tags=["tasks"])

    @app.get("/")
    def read_root():
        return {"message": "Todo API - Welcome!"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )