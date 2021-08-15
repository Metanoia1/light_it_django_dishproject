from rest_framework.serializers import ValidationError

from dishes.models import Dish, Ingredient


def has_numbers(string):
    if any(char.isdigit() for char in string):
        raise ValidationError("the dish title cannot contain the numbers")


def already_exists(string):
    if Dish.objects.filter(title=string):
        raise ValidationError("dish with this title already exists")


def correct_amount(value):
    try:
        value = int(value)
        if value > 10000 or value < 0:
            raise ValidationError("the `amount` should be between 0 and 10000")
    except ValueError:
        raise ValidationError("the amount value should be an integer")


def is_title_exists(string):
    if not Ingredient.objects.filter(title=string):
        raise ValidationError(f"Ingredient title '{string}' does not exists")
