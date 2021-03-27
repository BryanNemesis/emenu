from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    preparation_time = models.DurationField(null=False)
    is_vegetarian = models.BooleanField(null=False, default=False)
    date_added = models.DateField(auto_now_add=True, null=False)
    date_updated = models.DateField(auto_now=True, null=False)

    def __str__(self):
        return f'Dish no. {self.id}: {self.name}'


class Menu(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    dishes = models.ManyToManyField(Dish)
    description = models.CharField(max_length=1000)
    date_added = models.DateField(auto_now_add=True, null=False)
    date_updated = models.DateField(auto_now=True, null=False)

    def __str__(self):
        return f'Menu no. {self.id}: {self.name}'
