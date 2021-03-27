from datetime import timedelta

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from .models import Dish, Menu


class MenuApiTests(APITestCase):
    def setUp(self):
        client = APIClient(SERVER_NAME='localhost')
        d1 = Dish.objects.create(
            name='Stew', price='5', preparation_time=timedelta(minutes=30))
        d2 = Dish.objects.create(
            name='Sandwich', price='2', preparation_time=timedelta(minutes=15))
        d3 = Dish.objects.create(
            name='Sriracha', price='15', preparation_time=timedelta(seconds=5))
        m1 = Menu.objects.create(name="Main menu", description='Our famous menu')
        m2 = Menu.objects.create(name="Secret menu", description='Our secret menu')
        m1.dishes.set(d[:2])
        m2.dishes.set(d[2:])


    def some_test_case(self):
        self.assertEqual(1, 1)