from fastapi import FastAPI
from app.api.v1.message_routes import router

app = FastAPI()

app.include_router(router)
