from fastapi import FastAPI, Request
from app.routes import router
from app.middleware.logging import logging_middleware

app = FastAPI()

app.include_router(router)

app.middleware("http")(logging_middleware)

@app.get("/")
def base_response():
    return {"message":"Hey! This is EGO Services API. Visit /docs to learn about our API!"}
