from django.db import models


class Ingredient(models.Model):
    title = models.CharField(max_length=50)

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
    title = models.CharField(max_length=50, unique=True)
    ingredients = models.ManyToManyField(
        Ingredient,
        through="OrderIngredient",
    )

    def __str__(self):
        return self.title


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)


class OrderIngredient(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
