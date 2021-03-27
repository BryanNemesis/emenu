from django.db import models


class Dish(models.Model):
    pass


class Menu(models.Model):
    dishes = models.ManyToManyField(Dish)
