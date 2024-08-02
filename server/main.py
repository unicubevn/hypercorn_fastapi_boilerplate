from typing import Union

from dotenv import dotenv_values
from fastapi import FastAPI
from fastapi.datastructures import Default
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from hypercorn import logging
from hypercorn.config import Config

from models.api import UniCubeBaseResponse, ErrorResponse
from server.doc_metadata import tags_metadata, servers_metadata
from routers.api import router as api_router
from routers.auth import router as auth_router

_logger = logging.Logger(Config())
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000"
]

# Meta for docs
description = """
UniCube API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""
env = dotenv_values("./configs/dev_config.toml")
app = FastAPI(
    debug=env["ENVIRONMENT"] == "dev",
    default_response_class=Default(ORJSONResponse),
    title="UniCube Apis",
    description=description,
    openapi_url="/api/v1/openapi.json",
    openapi_tags=tags_metadata,
    servers=servers_metadata,
    summary="UniCube Apis for daily user",
    version="0.0.1",
    terms_of_service="https://unicube.vn/terms/",
    contact={
        "name": "UniCube JSC",
        "url": "https://unicube.vn/contact/",
        "email": "community@unicube.me",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
    responses={
        200: { "description": "Successful Response"},
        400: {"model": ErrorResponse, "description": "Invalid Item ID"},
        404: {"model": ErrorResponse, "description": "Item not found"}
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include api path
app.include_router(auth_router, tags=["Auth"], prefix="/auth")
app.include_router(api_router, tags=["Api"], prefix="/api")


@app.get("/", tags=["Api"])
async def read_root():
    await _logger.debug("hello world")
    return {"msg": "Hello World. This is UniCube Open Api"}
