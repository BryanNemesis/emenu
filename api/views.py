from datetime import datetime

from django.db.models import Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Menu
from .serializers import MenuListSerializer, MenuDetailSerializer, MenuCreateSerializer


class MenuList(ListCreateAPIView):
    """
    Get list of non-empty menus with GET, or create a new one with POST.
    """
    # permission_classes = [IsAuthenticatedOrReadOnly] 

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MenuListSerializer
        else:
            return MenuCreateSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            qs = Menu.objects.exclude(dishes__isnull=True)
            return filter_menu_queryset(qs, self.request.query_params)
        else:
            return Menu.objects.all()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                'sort_by',
                description='Choose to sort list by name or dish count, descending',
                enum=['name', 'dish_count']
                ),
            OpenApiParameter(
                'updated_after',
                description='View only menus created after a date in YYYY-MM-DD format'
                ),
            OpenApiParameter(
                'added_after',
                description='View only menus updated after a date in YYYY-MM-DD format'
                ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MenuDetail(RetrieveUpdateAPIView):    
    """
    Get details of a menu with GET, or edit it with PUT or PATCH.
    """
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MenuDetailSerializer
        else:
            return MenuCreateSerializer


def filter_menu_queryset(qs, query_params):
    """
    Handle filtering of queryset for menu list endpoint.
    """
    sort_by = query_params.get('sort_by')
    added_after = query_params.get('added_after')
    updated_after = query_params.get('updated_after')
    if added_after:
        qs = qs.filter(date_added__gt=datetime.strptime(added_after, '%Y-%m-%d'))
    if updated_after:
        qs = qs.filter(date_updated__gt=datetime.strptime(updated_after, '%Y-%m-%d')) 
    if sort_by == 'name':
        qs = qs.order_by('name')
    elif sort_by == 'dish_count':
        qs = qs.annotate(Count('dishes')).order_by('-dishes__count') 
    return qs