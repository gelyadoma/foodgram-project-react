# Generated by Django 3.2.18 on 2023-06-06 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20230605_1705'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='IngredientInRecipe',
            new_name='IngredientsInRecipe',
        ),
    ]
