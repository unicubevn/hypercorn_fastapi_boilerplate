#/models.py
from typing import List, Optional

from pydantic import BaseModel, EmailStr

class UserCredentials(BaseModel):
    username: str
    password: str
    scopes: List[str]=["openid"]
class User(BaseModel):
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    realm_roles: list
    client_roles: list


class authConfiguration(BaseModel):
    server_url: str
    realm: str
    client_id: str
    client_secret: str
    authorization_url: str
    token_url: str
    username: str
    password:  str
    description: str
    scopes: str = "openid"
