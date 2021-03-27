from django.urls import path

from .views import menu_list, menu_detail

urlpatterns = [
    path('', menu_list, name='menu_list'),
    path('<int:menu_id>/', menu_detail, name='menu_detail'),
    ]