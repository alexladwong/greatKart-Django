from django.shortcuts import render
from estores.models import *


# Create your views here.
def Home(request):
    products = (
        Products.objects.all().filter(is_available=True).order_by("-created_date")
    )

    # Fetch the Product Reviews and the stars
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        "products": products,
        "reviews": reviews,
    }
    return render(request, "store/index.html", context)
