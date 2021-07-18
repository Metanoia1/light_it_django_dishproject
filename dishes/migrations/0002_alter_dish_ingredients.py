# Generated by Django 3.2.5 on 2021-07-17 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dishes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dish",
            name="ingredients",
            field=models.ManyToManyField(
                related_name="ingredients",
                through="dishes.DishIngredient",
                to="dishes.Ingredient",
            ),
        ),
    ]
