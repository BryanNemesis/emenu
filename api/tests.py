from datetime import timedelta, date

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from .models import Dish, Menu


User = get_user_model()

class MenuApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='someuser', password='somepassword')
        self.client = APIClient(SERVER_NAME='localhost')
        self.client.force_authenticate(user=self.user)


    @classmethod
    def setUpTestData(cls):
        d1 = Dish.objects.create(name='Stew', price='5', preparation_time=timedelta(minutes=30))
        d2 = Dish.objects.create(name='Sandwich', price='2', preparation_time=timedelta(minutes=15))
        d3 = Dish.objects.create(name='Sriracha', price='15', preparation_time=timedelta(seconds=5))
        m1 = Menu.objects.create(name='Main menu')
        m2 = Menu.objects.create(name='Another menu')
        m3 = Menu.objects.create(name='Secret menu')
        m4 = Menu.objects.create(name='Empty menu')
        m1.dishes.set([d1, d2])
        m2.dishes.set([d1])
        m3.dishes.set([d1, d2, d3])


    def test_menu_list(self):
        url = reverse('menu_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)


    def test_menu_list_name_sort(self):
        url = reverse('menu_list') + '?sort_by=name'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Another menu')


    def test_menu_list_dish_count_sort(self):
        url = reverse('menu_list') + '?sort_by=dish_count'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Secret menu')


    def test_menu_filter_date_added(self):
        url = reverse('menu_list') + f'?added_after={str(date.today())}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)


    def test_menu_filter_date_updated(self):
        url = reverse('menu_list') + f'?updated_after={str(date.today())}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)


    def test_menu_create(self):
        url = reverse('menu_list')
        data = {'name': 'Breakfast menu', 'description': 'Breakfast menu'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Breakfast menu')
        self.assertEqual(len(Menu.objects.all()), 5)


    def test_menu_create_bad_data(self):
        url = reverse('menu_list')
        data = {'menu': 'Breakfast menu', 'description': 'Breakfast menu'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(Menu.objects.all()), 4)


    def test_menu_detail(self):
        url = reverse('menu_detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Main menu')
        self.assertEqual(len(response.data['dishes']), 2)


    def test_menu_detail_wrong_id(self):
        url = reverse('menu_detail', args=[5])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_menu_update_put(self):
        url = reverse('menu_detail', args=[1])
        data = {'name': 'New main menu', 'description': '', 'dishes': []}
        response = self.client.put(url, data)
        obj = Menu.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'New main menu')
        self.assertEqual(obj.name, 'New main menu')


    def test_menu_update_put_bad_data(self):
        url = reverse('menu_detail', args=[1])
        data = {'name': 'New main menu', 'description': '', 'dishes': 'fries'}
        response = self.client.put(url, data)
        obj = Menu.objects.first()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(obj.name, 'Main menu')


    def test_menu_update_patch(self):
        url = reverse('menu_detail', args=[1])
        data = {'dishes': ['Stew', 'Sandwich', 'Sriracha']}
        response = self.client.patch(url, data)
        obj = Menu.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['dishes']), 3)
        self.assertEqual(obj.dishes.count(), 3)


    def test_menu_update_patch_bad_data(self):
        url = reverse('menu_detail', args=[1])
        data = {'dishes': 'fries'}
        response = self.client.put(url, data)
        obj = Menu.objects.first()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(obj.dishes.count(), 2)