from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from ..database.connection import create_db_and_tables
from .routers import todos
from ..utils.errors import UNAUTHORIZED_RESPONSE, FORBIDDEN_RESPONSE, NOT_FOUND_RESPONSE, BAD_REQUEST_RESPONSE


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan event handler to run startup and shutdown events.
    """
    # Startup
    print("Starting up the application...")
    create_db_and_tables()
    print("Database tables created successfully.")
    
    yield  # Application runs here
    
    # Shutdown
    print("Shutting down the application...")


# Create the FastAPI application
app = FastAPI(
    title="Todo API",
    description="Secure, user-scoped REST API for Todo management",
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Todo API Support",
        "email": "support@todoapi.example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Allow Authorization header for JWT
    expose_headers=["Access-Control-Allow-Origin"]
)


# Include the todos router
app.include_router(
    todos.router,
    prefix="/api/v1",
    tags=["todos"],
    responses={
        401: UNAUTHORIZED_RESPONSE,
        403: FORBIDDEN_RESPONSE,
        404: NOT_FOUND_RESPONSE,
        400: BAD_REQUEST_RESPONSE
    }
)


@app.get("/")
def read_root():
    """
    Root endpoint for health check.
    """
    return {"message": "Todo API is running!"}


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "message": "Todo API is operational",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
    )


# Custom exception handlers
@app.exception_handler(404)
async def custom_http_exception_handler(request, exc):
    """
    Custom handler for 404 errors.
    """
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Resource not found or not owned by user",
            "error_code": "NOT_FOUND",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(422)
async def validation_exception_handler(request, exc):
    """
    Custom handler for validation errors.
    """
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "error_code": "VALIDATION_ERROR",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
    )
