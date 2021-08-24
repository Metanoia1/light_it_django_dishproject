from django.db.models import Count

from dishes.models import Dish


def get_most_popular_dishes(top_number: int):
    return (
        Dish.objects.all()
        .annotate(orders_count=Count("orders"))
        .order_by("-orders_count")[:top_number]
    )
