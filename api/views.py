from datetime import datetime

from django.db.models import Count
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Menu, Dish
from .serializers import MenuListSerializer, MenuDetailSerializer, MenuCreateSerializer


class MenuList(ListCreateAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.exclude(dishes__isnull=True)
    serializer_class = MenuCreateSerializer

    def list(self, request):
        qs = self.get_queryset()

        added_after = request.query_params.get('added_after')
        if added_after:
            qs = qs.filter(date_added__gt=datetime.strptime(added_after, '%Y-%m-%d'))
        updated_after = request.query_params.get('updated_after')
        if updated_after:
            qs = qs.filter(date_updated__gt=datetime.strptime(updated_after, '%Y-%m-%d')) 

        sort_by = request.query_params.get('sort_by')
        if sort_by == 'name':
            qs = qs.order_by('name')
        elif sort_by == 'dish_count':
            qs = qs.annotate(Count('dishes')).order_by('-dishes__count') 

        serializer = MenuListSerializer(qs, many=True)
        return Response(serializer.data)


class MenuDetail(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Menu.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return MenuDetailSerializer
        else:
            return MenuCreateSerializer
