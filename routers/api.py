from fastapi import APIRouter
from hypercorn.logging import Logger
from hypercorn.config import Config

router = APIRouter()

_logger = Logger(Config())


@router.get("/", )
async def get_ipn_list() -> str:
    await _logger.info("IPN service is running...")
    await _logger.debug("IPN")
    return "ipn router"

