from fastapi import FastAPI
from app.router import api_router
from app.db.connection import Base, engine

import app.models

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(api_router)