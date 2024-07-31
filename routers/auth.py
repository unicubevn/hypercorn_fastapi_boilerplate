import logging

from fastapi import APIRouter, Depends
from hypercorn import logging
from hypercorn.config import Config

from dependencies.auth import get_user_info, get_token
from models.keycloak import User, UserCredentials

router = APIRouter()

_logger = logging.Logger(Config())


@router.post("/token")
async def root(user_credentials: UserCredentials):
    await _logger.info("token is running ...")
    await _logger.info(user_credentials)
    token = await get_token(user_credentials)
    await _logger.info(token)
    return token
@router.get("/secure",)
async def root(user: User = Depends(get_user_info)):
    await _logger.info(f"user: {user}")
    if user:
        return {"message": f"Hello {user.username} you have the following service: {user.realm_roles}"}
    else:
        return {"message": "No User information"}