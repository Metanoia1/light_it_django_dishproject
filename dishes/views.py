from django.shortcuts import render, get_object_or_404, redirect
from . import models


def index(request):
    dishes = models.Dish.objects.all()
    context = {"dishes": dishes}
    return render(request, "dishes/index.html", context)


# ЭТА ВЬЮШКА ГЕНЕРИТ ОГРОМНОЕ КОЛ-ВО ЗАПРОСОВ К БАЗЕ И ТРЕБУЕТ ОПТИМИЗАЦИИ!!!
# def dish_details(request, dish_id):
#     dish = get_object_or_404(models.Dish, pk=dish_id)
#     ingredients = models.DishIngredient.objects.filter(dish__id=dish_id)
#     context = {"ingredients": ingredients}
#     if request.method == "POST":
#         order = models.Order.objects.create()
#         order.ingredients.set(dish.ingredients.all())
#         order_ingredient = models.OrderIngredient.objects.filter(
#             order__id=order.id
#         )
#         for order in order_ingredient:
#             order.amount = request.POST[str(order.ingredient)]
#             order.save()
#         return redirect("dishes:index")
#     return render(request, "dishes/details.html", context)


def orders(request):
    orders_list = models.OrderIngredient.objects.all()
    context = {"orders": orders_list}
    return render(request, "dishes/orders.html", context)


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
    return render(request, "dishes/details1.html", context)
