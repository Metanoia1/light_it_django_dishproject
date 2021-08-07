from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.contrib import messages
from django.utils.translation import gettext as _

from .forms import OrderIngredientModelForm
from .models import OrderIngredient, Order


INCORRECT_VALUE_MSG = "incorrect value"
TRY_YYYY_MM_DD_MSG = "try yyyy-mm-dd format"


def filter_gt(content, request, dishes):
    try:
        gt_content = content.get("gt", None)
        dishes = dishes.filter(created_at__gt=gt_content)
    except ValidationError:
        if gt_content:
            messages.info(
                request,
                f'{INCORRECT_VALUE_MSG} "{gt_content}" {TRY_YYYY_MM_DD_MSG}',
            )
    return dishes


def filter_lt(content, request, dishes):
    try:
        lt_content = content.get("lt", None)
        dishes = dishes.filter(created_at__lt=lt_content)
    except ValidationError:
        if lt_content:
            messages.info(
                request,
                f'{INCORRECT_VALUE_MSG} "{lt_content}" {TRY_YYYY_MM_DD_MSG}',
            )
    return dishes


def get_oi_formset(*, extra, max_num):
    return modelformset_factory(
        OrderIngredient,
        form=OrderIngredientModelForm,
        extra=extra,
        max_num=max_num,
    )


def get_oi_initial(ingredients):
    return [
        {"ingredient": item.ingredient, "amount": item.amount}
        for item in ingredients
    ]


def merge_instances_with_order(instances, order):
    for obj in instances:
        obj.order = order


def create_csv_report(writer, gt_date, queryset):
    writer.writerow(
        [
            "ORDER",
            "CREATED_AT",
            "DISH_TITLE",
            "INGREDIENTS",
            "CHANGED",
            "WHAT_IS_CHANGED",
        ]
    )
    for order in queryset.filter(created_at__gt=gt_date):
        dish = order.dish
        di = [f"{obj.ingredient.title}-{obj.amount}" for obj in dish.di.all()]
        oi = [f"{obj.ingredient.title}-{obj.amount}" for obj in order.oi.all()]
        is_changed = False
        changed_ingredients = []

        for string in oi:
            if string not in di:
                is_changed = True
                changed_ingredients.append(string)

        row = [
            order.id,
            order.created_at,
            order.dish.title,
            " ".join(di),
            is_changed,
            " ".join(changed_ingredients),
        ]

        writer.writerow(row)
