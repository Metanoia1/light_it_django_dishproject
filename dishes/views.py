import logging
import csv
import codecs
from datetime import timedelta

from django.urls import reverse
from django.core.cache import caches
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils.timezone import now

from django.utils.translation import gettext as _
from django.http import HttpResponse

from .models import Dish, Order, OrderIngredient
from . import utils


logger = logging.getLogger(__name__)


def login_user(request):
    if request.user.is_authenticated:
        return redirect("dishes:index")
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            content = request.GET
            if "next" in content:
                return redirect(content["next"])
            return redirect("dishes:index")
        messages.info(request, "incorrect login or password")
        logger.warning("incorrect login or password")
    return render(request, "dishes/login.html", {"form": AuthenticationForm()})


def register_user(request):
    if request.user.is_authenticated:
        return redirect("dishes:index")
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dishes:login")
    return render(request, "dishes/register.html", {"form": form})


@login_required(login_url="dishes:login")
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("dishes:index")
    return render(request, "dishes/logout_confirm.html")


class DishList(ListView):
    model = Dish
    template_name = "dishes/index.html"
    context_object_name = "dishes"

    def get_queryset(self):
        content = self.request.GET
        db_cache = caches["db_cache"]
        dishes = db_cache.get("dishes_list", [])

        if not dishes:
            dishes = Dish.objects.all()
            db_cache.set("dishes_list", dishes, 60)

        if "title" in content:
            return Dish.objects.filter(title=content.get("title", None))
        return dishes


class DishDetail(DetailView):
    model = Dish
    template_name = "dishes/details.html"
    context_object_name = "dish"

    def get_queryset(self):
        return Dish.objects.prefetch_related("di__ingredient")


class OrderList(LoginRequiredMixin, ListView):
    model = Order
    template_name = "dishes/orders.html"
    context_object_name = "orders"
    login_url = "/dishes/login/"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.request.user.orders.prefetch_related("oi__ingredient")
        return Order.objects.none()


class DishFilter(ListView):
    model = Dish
    template_name = "dishes/filters.html"
    context_object_name = "dishes"

    def get_queryset(self):
        content = self.request.GET
        dishes = Dish.objects.filter(title__icontains=content.get("title", ""))

        if "gt" in content:
            dishes = utils.filter_gt(content, self.request, dishes)

        if "lt" in content:
            dishes = utils.filter_lt(content, self.request, dishes)

        return dishes[::-1] if "reverse" in content else dishes


@login_required(login_url="dishes:login")
def create_order(request, dish_id):
    logger.debug("create_order called...")
    dish = get_object_or_404(Dish, pk=dish_id)
    ingredients = dish.di.select_related("ingredient")
    amount = ingredients.count()
    OrderIngredientFormSet = utils.get_oi_formset(extra=amount, max_num=amount)

    if request.method == "POST":
        formset = OrderIngredientFormSet(request.POST)
        if formset.is_valid():
            order = Order.objects.create(dish_id=dish.id, user=request.user)
            instances = formset.save(commit=False)
            utils.merge_instances_with_order(instances, order)
            formset.save()
            return redirect("dishes:orders")
        logger.warning("formset is not valid with data: %s", request.POST)
        return redirect("dishes:order", dish_id)

    context = {
        "title": _("ORDER CREATION"),
        "dish": dish,
        "formset": OrderIngredientFormSet(
            queryset=OrderIngredient.objects.none(),
            initial=utils.get_oi_initial(ingredients),
        ),
    }

    return render(request, "dishes/create_order.html", context)


@login_required(login_url="dishes:login")
def get_csv_report(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="report.csv"'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, delimiter=",")
    gt_date = now() - timedelta(days=1)

    if request.user.is_authenticated:
        queryset = request.user.orders.all()
    else:
        queryset = Order.objects.none()

    utils.create_csv_report(writer, gt_date, queryset)
    return response
