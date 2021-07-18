from django.shortcuts import render, get_object_or_404, redirect
from . import models


def index(request):
    dishes = models.Dish.objects.all()
    context = {"dishes": dishes}
    return render(request, "dishes/index.html", context)


def dish_details(request, dish_id):
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

        return redirect("dishes:index")
    ingredients = dish.di.all()
    context = {"ingredients": ingredients}
    return render(request, "dishes/dish_details.html", context)


# def orders(request):
#     orders_list = models.OrderIngredient.objects.all()
#     context = {"orders": orders_list}
#     return render(request, "dishes/orders.html", context)


def orders(request):
    order_list = models.Order.objects.all()
    context = {"orders": order_list}
    return render(request, "dishes/orders.html", context)
