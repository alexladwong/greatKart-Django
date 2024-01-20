from django.urls import path
from . import views

urlpatterns = [
    path("place_order/", views.Place_Orders, name="place_order"),
    path("payments/", views.Payments, name="payments"),
]
