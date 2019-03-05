import json
from argparse import ArgumentParser

from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('username')
        parser.add_argument('password')
        parser.add_argument('tenant_id')

    def handle(self, *args, **options):
        username = options.get('username')
        password = options.get('password')
        tenant_id = options.get('tenant_id')

        d = json.dumps({
            "auth": {
                "passwordCredentials": {
                    "username": username,
                    "password": password
                },
                "tenantId": tenant_id
            }
        })

        response = requests.post(
            url='https://identity.tyo1.conoha.io/v2.0/tokens',
            data=d,
            headers={'Content-Type': 'application/json'}
        )

        print(response.text)
