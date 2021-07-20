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


class OrderList(ListView):
    model = models.Order
    template_name = "dishes/orders.html"
    context_object_name = "orders"


def create_order(request, dish_id):
    dish = get_object_or_404(models.Dish, pk=dish_id)
    if request.method == "POST":
        order = models.Order.objects.create()
        order_ingredient_list = []

        for item in dish.di.all():
            order_ingredient = models.OrderIngredient(
                order=order,
                amount=request.POST[item.ingredient.title],
                ingredient=item.ingredient,
            )
            order_ingredient_list.append(order_ingredient)

        models.OrderIngredient.objects.bulk_create(order_ingredient_list)

        return redirect("dishes:orders")
    return render(request, "dishes/dish_details.html", {"dish": dish})
