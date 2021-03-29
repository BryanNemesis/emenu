from datetime import timedelta

from django.db import migrations, models

from ..models import Dish, Menu


def create_initial_data(apps, schema_editor):

    d1 = Dish.objects.create(name='Soup', price='5.99',
        description='Delicious soup', preparation_time=timedelta(minutes=20))
    d2 = Dish.objects.create(name='Chicken', price='15.99',
        description='Crispy chicken', preparation_time=timedelta(hours=1))
    d3 = Dish.objects.create(name='Ice cream', price='3.99',
        description='Strawberry ice cream', preparation_time=timedelta(seconds=30))

    m1 = Menu.objects.create(name='Main menu',
        description='The current main menu')
    m2 = Menu.objects.create(name='Special menu',
        description='Menu for special occasions')
    m3 = Menu.objects.create(name='Secret menu',
        description="Secret menu. Don't tell anyone")
    m4 = Menu.objects.create(name='Empty menu')

    m1.dishes.set([d1, d2])
    m2.dishes.set([d1, d2, d3])
    m3.dishes.set([d3])


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('preparation_time', models.DurationField()),
                ('is_vegetarian', models.BooleanField(default=False)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('dishes', models.ManyToManyField(to='api.Dish')),
            ],
        ),
        migrations.RunPython(create_initial_data),
    ]
