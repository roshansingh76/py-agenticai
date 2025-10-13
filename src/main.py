from fastapi import FastAPI
from src.routes.main_router import router as main_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    root_path='/agenticai',
    title="Py-Agentic AI",
    version="1.0.0",
    description="FastAPI app with modular routing"
)

origins = [
    "http://localhost:3000",  # React frontend
    # you can add other allowed origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # or ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include all routers
app.include_router(main_router, prefix="/api/v1")

