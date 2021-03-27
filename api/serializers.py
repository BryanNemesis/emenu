from rest_framework import serializers

from .models import Dish, Menu


class MenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            'name',
            'description',
            'dish_count',
            ]

    dish_count = serializers.SerializerMethodField(read_only=True)

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
