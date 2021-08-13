from django_filters.rest_framework import FilterSet, CharFilter, DateTimeFilter

from dishes.models import Dish


class DishDateTimeFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="exact")
    min_date = DateTimeFilter(field_name="created_at", lookup_expr="gt")
    max_date = DateTimeFilter(field_name="created_at", lookup_expr="lt")

    class Meta:
        model = Dish
        fields = ["title", "created_at"]
