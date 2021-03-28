from django.urls import path

from .views import MenuList, MenuDetail

urlpatterns = [
    path('', MenuList.as_view(), name='menu_list'),
    path('<int:pk>/', MenuDetail.as_view(), name='menu_detail'),
    ]