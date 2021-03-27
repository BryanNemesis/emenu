from datetime import datetime

from django.db.models import Count
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Menu, Dish
from .serializers import MenuListSerializer, MenuDetailSerializer, MenuCreateSerializer


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def menu_list(request):
    """
    View all menus with GET, or add a new one with POST.
    GET parameters:
     * sort_by
     name - to sort by menu name, alphabetically
     dish_count - to sort by number of dishes on a menu, descending
    """
    if request.method == 'GET':
        # TODO: only view not empty menus.
        # TODO: probably this could be done more effictiently...
        sort_by = request.query_params.get('sort_by')
        if sort_by == 'name':
            qs = Menu.objects.all().order_by('name')
        elif sort_by == 'dish_count':
            qs = Menu.objects.all().annotate(Count('dishes')).order_by('-dishes__count')
        else:
            qs = Menu.objects.all()

        added_after = request.query_params.get('added_after')
        if added_after:
            qs = qs.filter(date_added__gt=datetime.strptime(added_after, '%Y-%m-%d'))

        updated_after = request.query_params.get('updated_after')
        if updated_after:
            qs = qs.filter(date_updated__gt=datetime.strptime(updated_after, '%Y-%m-%d'))  

        serializer = MenuListSerializer(qs, many=True)
        return Response(serializer.data, status=200)
    
    if request.method == 'POST':
        serializer = MenuCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({}, status=400)


@api_view(['GET', 'PATCH'])
# @permission_classes([IsAuthenticatedOrReadOnly])
def menu_detail(request, menu_id):
    """
    View an existing menu with GET, or update it with PATCH.
    """
    try:
        menu = Menu.objects.get(id=menu_id)
    except Menu.DoesNotExist:
        return Response({}, status=404) 

    if request.method == 'GET':
        serializer = MenuDetailSerializer(menu)
        return Response(serializer.data, status=200)

    if request.method == 'PATCH':
        serializer = MenuCreateSerializer(menu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response({}, status=400)
