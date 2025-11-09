from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.routes.main_router import router as main_router
from src.config import settings
from dotenv import load_dotenv
import logging

# Load environment variables first
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    root_path=settings.root_path,
    title=settings.app_name,
    version=settings.app_version,
    description="FastAPI app with modular routing and best practices",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Using model: {settings.model_name}")


@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information"""
    logger.info(f"Shutting down {settings.app_name}")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "app": settings.app_name,
            "version": settings.app_version
        }
    )


# Include all routers
app.include_router(main_router, prefix="/api/v1")

