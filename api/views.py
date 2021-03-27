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
    """
    if request.method == 'GET':
        # TODO: add filtering options
        qs = Menu.objects.all()
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
