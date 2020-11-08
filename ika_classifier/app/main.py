from fastapi import FastAPI
from app.api.routes.IkaClassifier import classifier

app = FastAPI(openapi_url="/api/v1/classifier/openapi.json", docs_url="/api/v1/classifier/docs")

@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(classifier, prefix='/api/v1/classifier', tags=['classifier'])