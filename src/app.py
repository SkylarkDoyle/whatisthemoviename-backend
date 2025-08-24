from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from .routers import films

app = FastAPI(title="Film Recognition API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(films.router, prefix="/api/films", tags=["films"])
