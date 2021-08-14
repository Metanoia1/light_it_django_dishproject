from rest_framework.serializers import ValidationError

from dishes.models import Dish


def has_numbers(string):
    if any(char.isdigit() for char in string):
        raise ValidationError("the dish title cannot contain the numbers")


def already_exists(string):
    if Dish.objects.filter(title=string):
        raise ValidationError("dish with this title already exists.")
