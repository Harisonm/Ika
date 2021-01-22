from fastapi import FastAPI
from app.api.routes.IkaGmailStreamer import GmailStreamersApi
from app.api.routes.StreamProcess import StreamProcess
# from app.api.db import metadata, database, engine

# metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/streamers/openapi.json", docs_url="/api/v1/streamers/docs")

@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    pass

app.include_router(GmailStreamersApi, prefix='/api/v1/streamers', tags=['gmailStreamers'])
app.include_router(StreamProcess, prefix='/api/v1/streamers', tags=['streamProcess'])