# Generated by Django 3.2.5 on 2021-07-18 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dishes", "0005_remove_order_title"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="dishingredient",
            options={"ordering": ["-id"]},
        ),
        migrations.AlterModelOptions(
            name="orderingredient",
            options={"ordering": ["-id"]},
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="title",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
