from django.urls import path, reverse
from . import views


urlpatterns = [
    path("", views.estores, name="estores"),
    path("/<slug:category_slug>/", views.estores, name="products_by_category"),
    path(
        "/<slug:category_slug>/<slug:product_slug>/",
        views.Product_Details,
        name="products_details",
    ),
]
