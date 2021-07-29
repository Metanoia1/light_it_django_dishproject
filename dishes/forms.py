from django import forms

from . import models


class OrderIngredientModelForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(
        label="",
        queryset=models.Ingredient.objects.all(),
        to_field_name="title",
        widget=forms.TextInput(
            attrs={"class": "form-control", "readonly": "readonly"}
        ),
    )
    amount = forms.IntegerField(
        label="",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "max": 10000, "min": 0}
        ),
    )

    class Meta:
        model = models.OrderIngredient
        fields = ("ingredient", "amount")


# birth_date = forms.DateField(
#     widget=DateTimePicker(
#         options={"format": "YYYY-MM-DD", "pickSeconds": False}
#     )
# )
