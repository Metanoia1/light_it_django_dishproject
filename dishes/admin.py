from django.contrib import admin

from .models import Ingredient, Dish, Order, DishIngredient, OrderIngredient


class DishIngredientInline(admin.TabularInline):
    model = Dish.ingredients.through


class OrderIngredientInline(admin.TabularInline):
    model = Order.ingredients.through


class DishAdmin(admin.ModelAdmin):
    list_display = ("title",)
    inlines = [DishIngredientInline]


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id",)
    inlines = [OrderIngredientInline]


admin.site.register(Ingredient)
admin.site.register(Dish, DishAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(DishIngredient)
admin.site.register(OrderIngredient)
