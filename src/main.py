from fastapi import FastAPI
from src.routes.main_router import router as main_router

app = FastAPI(
    root_path='agentic_ai',
    title="Py-Agentic AI",
    version="1.0.0",
    description="FastAPI app with modular routing"
)

# Include all routers
app.include_router(main_router, prefix="/api/v1")

