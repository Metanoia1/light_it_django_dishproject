from django import forms

from . import models


class OrderIngredientForm(forms.ModelForm):
    class Meta:
        model = models.OrderIngredient
        fields = ["amount", "ingredient"]
