from fastapi import FastAPI
# from app.api.routes.IkaStreamer import streamers
from src.ika_streamer.app.api.routes.IkaStreamer import streamers
# from app.api.db import metadata, database, engine

# metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/streamers/openapi.json", docs_url="/api/v1/streamers/docs")

# @app.on_event("startup")
# async def startup():
#     pass

# @app.on_event("shutdown")
# async def shutdown():
#     pass

app.include_router(streamers, prefix='/api/v1/streamers', tags=['streamers'])