from datetime import datetime

import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from account.models import User
from upload.models import Video


class Command(BaseCommand):
    help = 'Mackerelでデータ集計する'

    def handle(self, *args, **options):
        headers = {
            'X-Api-Key': f"{settings.MACKEREL_KEY}",
            'Content-Type': 'application/json',
        }
        now = datetime.now()
        dataset = {
            'upload_count': {
                'all': Video.objects.all().count(),
                'today': Video.objects.filter(
                    profile__created_at__year=now.year,
                    profile__created_at__month=now.month,
                    profile__created_at__day=now.day
                ).count()
            },
            'user_count': {
                'all': User.objects.all().count(),
                'today': User.objects.filter(
                    date_joined__year=now.year,
                    date_joined__month=now.day,
                    date_joined__day=now.month
                ).count()
            }
        }
        time = now.timestamp()
        for name_prefix, data in dataset.items():
            json = []
            for name_key, value in data.items():
                name = f"custom.statistics.{name_prefix}.{name_key}"
                json.append({
                    'hostId': settings.MACKEREL_HOST_ID,
                    'name': name,
                    'time': time,
                    'value': value
                })
            response = requests.post('https://mackerel.io/api/v0/tsdb', json=json, headers=headers)
            response.raise_for_status()
