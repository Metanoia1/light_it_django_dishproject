from django.db import models


class Ingredient(models.Model):
    title = models.CharField(max_length=50)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title}|{self.amount}"


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


class OrderIngredient(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
