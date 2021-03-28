from django.db import models


class Dish(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    preparation_time = models.DurationField()
    is_vegetarian = models.BooleanField(default=False)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f'Dish no. {self.id}: {self.name}'


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dishes = models.ManyToManyField(Dish)
    description = models.CharField(max_length=1000, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f'Menu no. {self.id}: {self.name}'
