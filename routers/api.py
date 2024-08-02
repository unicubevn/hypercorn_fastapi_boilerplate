from typing import Optional

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from hypercorn.logging import Logger
from hypercorn.config import Config
from pydantic import BaseModel
from starlette.responses import JSONResponse

from models.api import UniCubeBaseResponse, TraceInfoBase, MetaData

router = APIRouter()

_logger = Logger(Config())


@router.get("/",response_model=UniCubeBaseResponse,
            response_model_exclude_none=True,
            )
async def root_api():
    await _logger.info("Open APi service is running...")
    await _logger.debug("IPN")
    return UniCubeBaseResponse(data=[{'hello': 'This is Api path'}], meta=MetaData())



