import jwt
from configs.configs import PRIVATE_KEY, PUBLIC_KEY


def encode_ES384(data, context=None):
    token = jwt.encode(data, key=PRIVATE_KEY, algorithm='ES384')
    token = str(token)
    if token.startswith("b'") and token.endswith("'"):
        return token[2:-1]
    else:
        return token



def decode_ES384(token, context=None):
    return jwt.decode(token, key=PUBLIC_KEY, algorithms='ES384', verify=True)
