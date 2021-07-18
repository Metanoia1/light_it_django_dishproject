from django.db import models


class Ingredient(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Dish(models.Model):
    title = models.CharField(max_length=50, unique=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through="DishIngredient",
    )

    def __str__(self):
        return self.title


class Order(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        through="OrderIngredient",
    )


class IngredientAmount(models.Model):
    amount = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True
        ordering = ["-id"]


class DishIngredient(IngredientAmount):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="ingredients"
    )


class OrderIngredient(IngredientAmount):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
