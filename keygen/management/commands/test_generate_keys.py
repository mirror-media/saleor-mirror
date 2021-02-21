from unittest import TestCase
import jwt
from generate_keys import generate_new_key
import string
import random


class Test(TestCase):
    def test_generate_new_key(self):
        letters = string.ascii_letters

        data = {"email": ''.join(random.choice(letters) for i in range(10)),
                "password": ''.join(random.choice(letters) for i in range(10))}
        public_serial, private_serial = generate_new_key()
        encrypt = jwt.encode(data, private_serial, algorithm='ES384')
        decrypt = jwt.decode(encrypt, key=public_serial, algorithms='ES384',
                             verify=True)
        self.assertEqual(data, decrypt)
