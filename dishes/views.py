from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView

from . import models


class DishList(ListView):
    model = models.Dish
    template_name = "dishes/index.html"
    context_object_name = "dishes"


class DishDetail(DetailView):
    model = models.Dish
    template_name = "dishes/details.html"
    context_object_name = "dish"

    def get_queryset(self):
        return models.Dish.objects.prefetch_related("di__ingredient")


class OrderCreation(DetailView):
    model = models.Dish
    template_name = "dishes/create_order.html"
    context_object_name = "dish"

    def get_queryset(self):
        return models.Dish.objects.prefetch_related("di__ingredient")


class OrderList(ListView):
    model = models.Order
    template_name = "dishes/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return models.Order.objects.prefetch_related("oi__ingredient")


def create_order(request, dish_id):
    dish = get_object_or_404(models.Dish, pk=dish_id)
    if request.method == "POST":
        order = models.Order.objects.create(dish_id=dish.id)

        models.OrderIngredient.objects.bulk_create(
            models.OrderIngredient(
                order=order,
                amount=request.POST[item.ingredient.title],
                ingredient=item.ingredient,
            )
            for item in dish.di.all()
        )

        return redirect("dishes:orders")
    return render(request, "dishes/details.html", {"dish": dish})
