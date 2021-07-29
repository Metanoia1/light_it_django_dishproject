import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from . import models
from . import utils


logger = logging.getLogger(__name__)


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
    logger.debug("create_order called...")
    dish = get_object_or_404(models.Dish, pk=dish_id)
    ingredients = dish.di.select_related("ingredient")
    amount = ingredients.count()
    OrderIngredientFormSet = utils.get_oi_formset(extra=amount, max_num=amount)

    if request.method == "POST":
        formset = OrderIngredientFormSet(request.POST)
        if formset.is_valid():
            order = models.Order.objects.create(dish_id=dish.id)
            instances = formset.save(commit=False)
            utils.merge_instances_with_order(instances, order)
            formset.save()
            return redirect("dishes:orders")
        logger.warning("formset is not valid")

    context = {
        "dish": dish,
        "formset": OrderIngredientFormSet(
            queryset=models.OrderIngredient.objects.none(),
            initial=utils.get_oi_initial(ingredients),
        ),
    }

    return render(request, "dishes/create_order.html", context)
