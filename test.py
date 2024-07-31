import jwt
from jwcrypto import jwk
from jwt.algorithms import RSAAlgorithm
from keycloak import KeycloakOpenID

from models.keycloak import authConfiguration

settings = authConfiguration(
    server_url="https://oid.unicube.vn/",
    realm="roc",
    client_id="rns:roc:portal",
    client_secret="MDBDx9CeLJBiZsgl8nVbNpBg0hf1m61r",
    authorization_url="https://oid.unicube.vn/realms/roc/protocol/openid-connect/auth",
    token_url="https://oid.unicube.vn/realms/roc/protocol/openid-connect/token",
    username="admin",
    password="Unicube1511@",
    description="""
        client_id="rns:roc:portal",
        client_secret="MDBDx9CeLJBiZsgl8nVbNpBg0hf1m61r",
        username="admin",
        password="Unicube1511@"
    """
)

keycloak_openid = KeycloakOpenID(
    server_url=settings.server_url,  # https://sso.example.com/auth/
    client_id=settings.client_id,  # backend-client-id
    realm_name=settings.realm,  # example-realm
    client_secret_key=settings.client_secret,  # your backend client secret
    verify=True

)
# jwks = keycloak_openid.certs()
# print(jwks)
# print(jwks['keys'][1]['alg'])
# public_key = RSAAlgorithm.from_jwk(jwks['keys'][1])
# print(public_key)
public_key = (
        "-----BEGIN PUBLIC KEY-----\n"
        + keycloak_openid.public_key()
        + "\n-----END PUBLIC KEY-----"
)


# Function to decode and verify JWT token
def verify_token(token):
    try:
        print(token)
        decoded_token = jwt.decode(token, public_key, algorithms=['RS256'], audience=settings.client_id)
        print(decoded_token)
        return decoded_token
    except jwt.ExpiredSignatureError:
        print('Token has expired')
    except Exception as e:
        print(e)


# token= "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJoN0E3VF9Tdms1RE5uVUQwcDA0ZGw1MlVEY29KQjFKbmdfdXAxelFrWWxZIn0.eyJleHAiOjE3MjIzNzk4MDQsImlhdCI6MTcyMjM3OTUwNCwianRpIjoiNDk3NGVlNjAtY2IyNy00YzEyLTkxMzAtMjY5MjUwMGRhOGJkIiwiaXNzIjoiaHR0cHM6Ly9vaWQudW5pY3ViZS52bi9yZWFsbXMvcm9jIiwiYXVkIjoiYWNjb3VudCIsInN1YiI6ImU1ZjMwYmMyLWRhZTEtNDNiNC1iZjNmLTYzZjVhZjM0ZTQ2ZCIsInR5cCI6IkJlYXJlciIsImF6cCI6InJuczpyb2M6cG9ydGFsIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLXJvYyIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHByb2ZpbGUiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImNsaWVudEhvc3QiOiIxNC4xNjkuNDAuMjQ3IiwicHJlZmVycmVkX3VzZXJuYW1lIjoic2VydmljZS1hY2NvdW50LXJuczpyb2M6cG9ydGFsIiwiY2xpZW50QWRkcmVzcyI6IjE0LjE2OS40MC4yNDciLCJjbGllbnRfaWQiOiJybnM6cm9jOnBvcnRhbCJ9.j1ifKRFJtoeZoX3gpFpkXiSAWVvUw5Ap0AA_tnU-MYXe94NHucIgl0F-LZ-sGqDpZdLUJc4Hmra7JtpxR-pb-IkJfDs85l8z05sbMsARJEE7SCsxywFIgPUsfbhkODset34xrdPWg85dAiAYnB3FyLSAnC-wbTl6xBA7B_7gZa5qjGX-H2-Mlixvfh_Q2iVdM6hE3C12mNxViqCiiShFiYk65lN1Gpg8SC96xdkVPGPrNFyGJXKCWF3En6AL9QBs2fIZWxZ468UUI13uTXXOrtaYGhrKbJMfnhCDh5l15jnCtyH50nNME-_zFy4xR7TwPB2fvZ4Pm0n_TLTVlZIbwQ"
token = keycloak_openid.token(grant_type="password", scope="openid profile email", username="admin",
                              password="Unicube1511@")
print(token)
print(public_key)
public_key = jwk.JWK.from_pem(public_key.encode("utf-8"))
decoded_token = keycloak_openid.decode_token(token['id_token'], key=public_key)
if decoded_token:
    print('Token is valid')
    print(decoded_token)
else:
    print('Token is invalid or expired')
