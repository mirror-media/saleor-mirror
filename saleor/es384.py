import jwt
from configs.configs import PRIVATE_KEY, PUBLIC_KEY


def encode_ES384(data, context=None):
    return jwt.encode(data, key=PRIVATE_KEY, algorithm='ES384')


def decode_ES384(token, context=None):
    return jwt.decode(token, key=PUBLIC_KEY, algorithms='ES384', verify=True)
