import jwt
from configs.configs import PRIVATE_KEY, PUBLIC_KEY
from django.conf import settings

JWT_ALGORITHM = settings.GRAPHQL_JWT["JWT_ALGORITHM"]

def encode_ES384(data, context=None):
    token = jwt.encode(data, key=PRIVATE_KEY, algorithm=JWT_ALGORITHM)
    token = str(token)
    if token.startswith("b'") and token.endswith("'"):
        return token[2:-1]
    else:
        return token



def decode_ES384(token, context=None):
    return jwt.decode(token, key=PUBLIC_KEY, algorithms=JWT_ALGORITHM, verify=True)
