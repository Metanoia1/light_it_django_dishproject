from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.views import View

from . import models


class DishList(ListView):
    model = models.Dish
    template_name = "dishes/index.html"
    context_object_name = "dishes"


class DishDetail(DetailView):
    model = models.Dish
    template_name = "dishes/dish_details.html"
    context_object_name = "dish"


class OrderList(ListView):
    model = models.Order
    template_name = "dishes/orders.html"
    context_object_name = "orders"


def create_order(request, dish_id):
    dish = get_object_or_404(models.Dish, pk=dish_id)
    if request.method == "POST":
        order = models.Order.objects.create()
        ingredients = dish.ingredients.all()

        for ingredient in ingredients:
            order.ingredients.add(ingredient)

        for order_ingredient in order.oi.all():
            order_ingredient.amount = request.POST[
                str(order_ingredient.ingredient)
            ]
            order_ingredient.save()
        return redirect("dishes:orders")

    return render(request, "dishes/dish_details.html", {"dish": dish})
