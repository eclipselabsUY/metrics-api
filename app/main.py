from fastapi import FastAPI, Request
from app.routes import router
from app.logging import logger

app = FastAPI()

app.include_router(router)


@app.get("/")
def base_response(request : Request):
    logger.info("Request recieved", extra={
        "method" : request.method, 
        "path" : request.url.path, 
        "client" : request.client.host if request.client else None
        })
    return {"message":"Hey! This is EGO Services API. Visit /docs to learn about our API!"}
