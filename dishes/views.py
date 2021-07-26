from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.forms import formset_factory

from .forms import OrderIngredientForm
from . import models
from . import utils


class DishList(ListView):
    model = models.Dish
    template_name = "dishes/index.html"
    context_object_name = "dishes"

    def get_queryset(self):
        content = self.request.GET
        if "title" in content:
            return models.Dish.objects.filter(title=content.get("title", None))
        return models.Dish.objects.all()


class DishDetail(DetailView):
    model = models.Dish
    template_name = "dishes/details.html"
    context_object_name = "dish"

    def get_queryset(self):
        return models.Dish.objects.prefetch_related("di__ingredient")


class OrderList(ListView):
    model = models.Order
    template_name = "dishes/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return models.Order.objects.prefetch_related("oi__ingredient")


class DishFilter(ListView):
    model = models.Dish
    template_name = "dishes/filters.html"
    context_object_name = "dishes"

    def get_queryset(self):
        content = self.request.GET
        dishes = models.Dish.objects.filter(
            title__icontains=content.get("title", "")
        )

        if "gt" in content:
            dishes = utils.filter_gt(content, self.request, dishes)

        if "lt" in content:
            dishes = utils.filter_lt(content, self.request, dishes)

        return dishes[::-1] if "reverse" in content else dishes


def create_order(request, dish_id):
    dish = get_object_or_404(models.Dish, pk=dish_id)
    ingredients = dish.di.all()
    FSet = formset_factory(OrderIngredientForm, max_num=ingredients.count())
    initial = [
        {"ingredient": item.ingredient.title, "amount": item.amount}
        for item in ingredients
    ]

    if request.method == "POST":
        formset = FSet(request.POST, initial=initial)
        if formset.is_valid():
            order = models.Order.objects.create(dish_id=dish.id)
            models.OrderIngredient.objects.bulk_create(
                models.OrderIngredient(
                    order=order,
                    ingredient=models.Ingredient.objects.get(
                        title=item["ingredient"]
                    ),
                    amount=item["amount"],
                )
                for item in formset.cleaned_data
            )
            return redirect("dishes:orders")

    context = {"dish": dish, "formset": FSet(initial=initial)}
    return render(request, "dishes/create_order.html", context)
