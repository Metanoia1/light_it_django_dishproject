from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from django.contrib import messages

from .forms import OrderIngredientModelForm
from .models import OrderIngredient


def filter_gt(content, request, dishes):
    try:
        gt_content = content.get("gt", None)
        dishes = dishes.filter(created_at__gt=gt_content)
    except ValidationError:
        if gt_content:
            messages.info(
                request,
                f"incorrect value '{gt_content}' try yyyy-mm-dd format",
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
                f"incorrect value '{lt_content}' try yyyy-mm-dd format",
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
