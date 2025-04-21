from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="Transfermarkt Player API",
    version="0.1"
)

app.include_router(router)
