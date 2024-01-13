from django.urls import path
from . import views

urlpatterns = [
    path("", views.Carts, name="carts"),
    path("add_cart/<int:product_id>/", views.Add_to_Cart, name="add_cart"),
    path("remove_cart/<int:product_id>/", views.Remove_Cart, name="remove_cart"),
    path("delete_cart_items/<int:product_id>/", views.Delete_Cart, name="delete_cart"),
]
