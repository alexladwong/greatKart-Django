from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import *
from store.models import *


# Create your views here.


def estores(request, category_slug=None):
    category = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Products.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Products.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        "products": products,
        "product_count": product_count,
    }
    return render(request, "estores/estores.html", context)


def Product_Details(request, category_slug, product_slug):
    try:
        single_product = Products.objects.get(
            category__slug=category_slug, slug=product_slug
        )
    except Exception as e:
        raise e
    context = {
        "single_product": single_product,
    }
    return render(request, "estores/product_details.html", context)
