import json
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.auth.models import User

from api.models import Dish
from api.serializers import DishDetailSerializer


class Command(BaseCommand):
    help = 'Sends an email to all users with info about recently modified dishes'

    def handle(self, *args, **options):
        yesterday = date.today() - timedelta(days=1)
        qs = Dish.objects.filter(date_updated=yesterday).filter(date_updated=yesterday)
        serializer = DishDetailSerializer(qs, many=True)
        emails = User.objects.filter(is_active=True).values_list('email', flat=True)

        message = f"""Hello,\n
        here's your daily list of dishes which were added or modified yesterday:\n\n
        {json.dumps(serializer.data, indent=4)}\n\n
        Greetings from the eMenu squad"""

        for email in emails:
            send_mail(
                subject = 'Daily eMenu report',
                message = message,
                from_email='mailbot@eMenu',
                recipient_list = [email],
                fail_silently=False,
            )
