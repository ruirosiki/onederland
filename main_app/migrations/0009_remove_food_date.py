# Generated by Django 4.2.1 on 2023-06-08 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_remove_food_date_added_food_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='date',
        ),
    ]