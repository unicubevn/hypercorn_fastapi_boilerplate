# /config.py
from models.keycloak import authConfiguration

settings = authConfiguration(
    server_url="https://oid.unicube.vn/",
    realm="roc",
    client_id="rns:roc:portal",
    client_secret="MDBDx9CeLJBiZsgl8nVbNpBg0hf1m61r",
    authorization_url="https://oid.unicube.vn/realms/roc/protocol/openid-connect/auth",
    token_url="https://oid.unicube.vn/realms/roc/protocol/openid-connect/token",
    username="",
    password="",
    description="""
        client_id="rns:roc:portal",
        client_secret="MDBDx9CeLJBiZsgl8nVbNpBg0hf1m61r",
        username="admin",
        password="Unicube1511@"
    """
)
