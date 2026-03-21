from fastapi import FastAPI
from src.router import main_router

import uvicorn

app = FastAPI()
app.include_router(main_router)

