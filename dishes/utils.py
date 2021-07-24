from django.core.exceptions import ValidationError
from django.contrib import messages


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
