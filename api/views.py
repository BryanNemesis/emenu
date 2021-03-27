from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Menu, Dish
from .serializers import MenuListSerializer, MenuDetailSerializer, MenuCreateSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def menu_list(request):
    """
    View all menus with GET, or add a new one with POST.
    """
    return Response()


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticatedOrReadOnly])
def menu_detail(request):
    """
    View an existing menu with GET, or update it with PATCH.
    """
    return Response()
