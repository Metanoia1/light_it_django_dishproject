from django import forms

from . import models


class OrderIngredientForm(forms.Form):
    ingredient = forms.CharField(
        label="",
        disabled=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    amount = forms.IntegerField(
        label="",
        min_value=0,
        max_value=10000,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
