from django.urls import path

from . import views


app_name = "dishes"

urlpatterns = [
    path("", views.DishList.as_view(), name="index"),
    path("filters/", views.DishFilter.as_view(), name="filters"),
    path("<int:pk>/", views.DishDetail.as_view(), name="details"),
    path("orders/", views.OrderList.as_view(), name="orders"),
    path("order/<int:dish_id>/", views.create_order, name="order"),
    path("report/", views.get_csv_report, name="report"),
    path("login/", views.login_user, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_user, name="logout"),
]
