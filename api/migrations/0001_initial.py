# Generated by Django 2.2 on 2021-03-27 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
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
                ('description', models.CharField(max_length=1000)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
                ('dishes', models.ManyToManyField(to='api.Dish')),
            ],
        ),
    ]