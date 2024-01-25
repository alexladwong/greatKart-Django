from django.urls import path, reverse
from . import views


urlpatterns = [
    path("", views.estores, name="estores"),
    path("category/<slug:category_slug>/", views.estores, name="products_by_category"),
    path(
        "category/<slug:category_slug>/<slug:product_slug>/",
        views.Product_Details,
        name="products_details",
    ),
    path("search-products/", views.Search, name="search"),
    # Customers Reviews
    path("submit-review/<int:product_id>/", views.CustomerReview, name="submit_review"),
]
