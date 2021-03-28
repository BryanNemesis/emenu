from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from .models import Dish, Menu


class MenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'name',
            'description',
            'dish_count',
            'date_added',
            'date_updated',
            ]

    dish_count = serializers.SerializerMethodField(read_only=True)

    @extend_schema_field(int)
    def get_dish_count(self, obj):
        return obj.dishes.count()
    

class DishDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = [
            'name',
            'description',
            'price',
            'preparation_time',
            'is_vegetarian',
            'date_added',
            'date_updated',
            ]


class MenuDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'name',
            'description',
            'date_added',
            'date_updated',
            'dishes',
            ]
        
    dishes = DishDetailSerializer(many=True)


class MenuCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'name',
            'description',
            'dishes',
        ]

    dishes = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Dish.objects.all())
