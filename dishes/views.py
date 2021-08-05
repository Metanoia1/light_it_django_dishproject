import logging
import csv
import codecs
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils.timezone import now
from django.http import HttpResponse

from .models import Dish, Order, OrderIngredient
from .utils import (
    merge_instances_with_order,
    create_csv_report,
    get_oi_formset,
    get_oi_initial,
    filter_gt,
    filter_lt,
)


logger = logging.getLogger(__name__)


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dishes:index')
        else:
            messages.info(request, 'login or password is incorrect')
    return render(request, 'dishes/login.html')


def register_user(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dishes:index')
    return render(request, 'dishes/register.html', {'form':form})


class DishList(ListView):
    model = Dish
    template_name = "dishes/index.html"
    context_object_name = "dishes"

    def get_queryset(self):
        content = self.request.GET
        if "title" in content:
            return Dish.objects.filter(title=content.get("title", None))
        return Dish.objects.all()


class DishDetail(DetailView):
    model = Dish
    template_name = "dishes/details.html"
    context_object_name = "dish"

    def get_queryset(self):
        return Dish.objects.prefetch_related("di__ingredient")


class OrderList(ListView):
    model = Order
    template_name = "dishes/orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.prefetch_related("oi__ingredient")


class DishFilter(ListView):
    model = Dish
    template_name = "dishes/filters.html"
    context_object_name = "dishes"

    def get_queryset(self):
        content = self.request.GET
        dishes = Dish.objects.filter(title__icontains=content.get("title", ""))

        if "gt" in content:
            dishes = filter_gt(content, self.request, dishes)

        if "lt" in content:
            dishes = filter_lt(content, self.request, dishes)

        return dishes[::-1] if "reverse" in content else dishes


def create_order(request, dish_id):
    logger.debug("create_order called...")
    dish = get_object_or_404(Dish, pk=dish_id)
    ingredients = dish.di.select_related("ingredient")
    amount = ingredients.count()
    OrderIngredientFormSet = get_oi_formset(extra=amount, max_num=amount)

    if request.method == "POST":
        formset = OrderIngredientFormSet(request.POST)
        if formset.is_valid():
            order = Order.objects.create(dish_id=dish.id)
            instances = formset.save(commit=False)
            merge_instances_with_order(instances, order)
            formset.save()
            return redirect("dishes:orders")
        logger.warning("formset is not valid with data: %s", request.POST)
        return redirect("dishes:order", dish_id)

    context = {
        "dish": dish,
        "formset": OrderIngredientFormSet(
            queryset=OrderIngredient.objects.none(),
            initial=get_oi_initial(ingredients),
        ),
    }

    return render(request, "dishes/create_order.html", context)


def get_csv_report(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="report.csv"'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, delimiter=",")
    gt_date = now() - timedelta(days=1)
    create_csv_report(writer, gt_date)
    return response
