from rest_framework.serializers import ValidationError


def has_numbers(string):
    if any(char.isdigit() for char in string):
        raise ValidationError("the dish title cannot contain the numbers")
