# /auth.py
from typing import Optional

import requests
from jose import JWTError, jwt
from hypercorn.logging import Logger
from hypercorn.config import Config

from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer, HTTPBearer, \
    HTTPAuthorizationCredentials
from jwcrypto import jwk
from keycloak import KeycloakOpenID  # pip require python-keycloak
from models.configs import settings
from fastapi import Security, HTTPException, status, Depends
from pydantic import Json
from models.keycloak import User, UserCredentials

_logger = Logger(Config())

# This is used for fastapi docs authentification
oauth2_scheme = OAuth2PasswordBearer(
    # authorizationUrl=settings.authorization_url, # https://sso.example.com/auth/
    tokenUrl=settings.token_url,  # https://sso.example.com/auth/realms/example-realm/protocol/openid-connect/token
    # scopes={'openid': 'OpenID'},
    description=settings.description,
    # client_id=settings.client_id,
    # client_secret=settings.client_secret,
    # grant_type='password',
    # username=settings.username,
    # password=settings.password
)

# This actually does the auth checks
# client_secret_key is not mandatory if the client is public on keycloak
keycloak_openid = KeycloakOpenID(
    server_url=settings.server_url,  # https://sso.example.com/auth/
    client_id=settings.client_id,  # backend-client-id
    realm_name=settings.realm,  # example-realm
    client_secret_key=settings.client_secret,  # your backend client secret
    verify=True

)


async def get_idp_public_key(static=False):
    if static:
        cert = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtZ3xs0aC0hnkw623m4VtAFMYOCFCWSeVwdIky2OQHYmYUth1D/d0FXfEv3l2QtaWcKorTf4nUBnapjJbLE20KF1KViC9+EbiHYwAJsoVFy98bopDXnGXACN3TRGhtj606z+oDE23mTuEJ/vBef2lPnlRmdkdDayX3D/WgCPjkH+cZJPh5UXbGkEsX6giP5LFqV8FFSkRrxAbayxr9EiMo1HnGPCOoe5F7SDWJXCun4FxYGAoB2We/3dFxCTL6nZC8kf1jEdDp5QatB7JNzPwQNls0JFGIcpcqBkgHlMglhVHERhl/Zp4ZobCh7+p4Sf/XLfIsthbLjZicLTmCOi9NQIDAQAB"
        # Fetch public key from Keycloak
        # jwks = keycloak_openid.certs()
        # for key in jwks['keys']:
        #     if key['kty'] == 'RSA':
        #         return jwt.algorithms.RSAAlgorithm.from_jwk(key)
        # raise ValueError('No RSA key found in JWKS')
    else:
        cert = (
            "-----BEGIN PUBLIC KEY-----\n"
            f"{keycloak_openid.public_key()}"
            "\n-----END PUBLIC KEY-----"
        )

    return jwk.JWK.from_pem(cert.encode("utf-8"))


# Get the payload/token from keycloak
# TODO: add token bearer to chec kauthen
async def get_payload(openid_token: Optional[str] = Security(oauth2_scheme, scopes=['openid']),
                      bearer_token: Optional[HTTPAuthorizationCredentials] = Security(HTTPBearer())) -> dict:
    try:
        token = None
        if openid_token:
            token = openid_token
        if bearer_token:
            await _logger.info("Bearer is running ...")
            token = bearer_token.credentials
        await _logger.info(f"Token: {token}")
        result = keycloak_openid.decode_token(token, key=await get_idp_public_key(), )

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_token(userCredential: UserCredentials) -> dict:
    try:
        print(userCredential)
        return keycloak_openid.token(userCredential.username, userCredential.password, grant_type='password',
                                     scope=userCredential.scopes)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Get user infos from the payload
async def get_user_info(payload: dict = Depends(get_payload)) -> User:
    try:
        return User(
            id=payload.get("sub", ""),
            username=payload.get("preferred_username", ""),
            email=payload.get("email", ""),
            first_name=payload.get("given_name", ""),
            last_name=payload.get("family_name", ""),
            realm_roles=payload.get("realm_access", {}).get("roles", []),
            client_roles=payload.get("realm_access", {}).get("roles", [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),  # "Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
