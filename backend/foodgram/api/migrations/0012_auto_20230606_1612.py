# Generated by Django 3.2.18 on 2023-06-06 13:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_ingredientinrecipe_ingredientsinrecipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='IngredientsInRecipe', to='api.ingredient'),
        ),
        migrations.AlterField(
            model_name='ingredientsinrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='IngredientsInRecipe', to='api.recipe'),
        ),
    ]
