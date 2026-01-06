from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import settings
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.utils.security import add_security_headers
from src.database.connection import create_db_and_tables

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    create_db_and_tables()
    app = FastAPI(
        title="Todo API",
        description="A full-stack todo web application with user authentication and task management capabilities",
        version="0.1.0",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
    )

    # Store the original openapi method to avoid recursion
    original_openapi = app.openapi

    # Add custom OpenAPI schema with security schemes for Swagger UI
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = original_openapi()

        # Ensure components exist
        if "components" not in openapi_schema:
            openapi_schema["components"] = {}
        if "securitySchemes" not in openapi_schema["components"]:
            openapi_schema["components"]["securitySchemes"] = {}

        # Add Bearer token security scheme
        openapi_schema["components"]["securitySchemes"]["HTTPBearer"] = {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter: Bearer {your JWT token}"
        }

        # Add security requirement to protected paths
        for path_name, path_item in openapi_schema.get("paths", {}).items():
            for method, operation in path_item.items():
                if path_name.startswith(f"{settings.api_prefix}/tasks"):  # Protect task endpoints
                    if "security" not in operation:
                        operation["security"] = [{"HTTPBearer": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

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