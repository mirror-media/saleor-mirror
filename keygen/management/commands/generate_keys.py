from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from django.core.management.base import BaseCommand
from django.conf import settings

# JWT_ALGORITHM = settings.GRAPHQL_JWT.get("JWT_ALGORITHM")
JWT_ALGORITHM = 'ES384'

def generate_new_key():
    """
    ECDSA using P-384 and SHA-384 (NIST curve, part of CNSA Suite, and approved to protect "top secret" systems)
    https://cryptography.io/en/latest/hazmat/primitives/asymmetric/ec.html
    Command line examples:
        # Generate private key
        openssl ecparam -name secp384r1 -genkey -noout -out jwtES384key.pem
        # Generate public key
        openssl ec -in jwtES384key.pem -pubout -out jwtES384pubkey.pub
    :return:
    """

    # TODO: algorithm is currently fixed to ES384, make this changeable
    private_key = ec.generate_private_key(ec.SECP384R1())
    public_key = private_key.public_key()

    public_serial = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                            format=serialization.PublicFormat.SubjectPublicKeyInfo).decode(
        'utf-8')

    private_serial = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()).decode('utf-8')
    return public_serial, private_serial


class Command(BaseCommand):
    help = "Generate new signing keys"

    def handle(self, *args, **options):
        try:
            public_serial, private_serial = generate_new_key()

            self.stdout.write(self.style.SUCCESS(f"Successfully created new keys for {JWT_ALGORITHM}: "))
            self.stdout.write(self.style.SUCCESS(public_serial))
            self.stdout.write(self.style.SUCCESS(private_serial))
        except Exception as e:

            self.stderr.write(self.style.ERROR(f"FAILED for {e.args[0]}"))

