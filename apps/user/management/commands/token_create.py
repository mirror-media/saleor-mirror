import json
from getpass import getpass

from django.core.management import BaseCommand

from saleor.schema import schema


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = input("EMAIL: ")
        password = getpass("PASSWORD: ", )
        gql = f"""
        mutation tokenCreate(email: "{email}", password:"{password}") {{
            token
            refreshToken
        }}
        """
        result = schema.execute(gql)
        items = dict(result.data.items())
        self.stdout(self.style.SUCCESS(json.dumps(items)))
