from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import *
from store.models import *
from carts.models import CartItem
from carts.views import _card_id


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
        in_cart = CartItem.objects.filter(
            cart__cart_id=_card_id(request), product=single_product
        ).exists()
        # return HttpResponse(in_cart)
        # exit()
    except Exception as e:
        raise e
    context = {
        "single_product": single_product,
        "in_cart": in_cart,
    }
    return render(request, "estores/product_details.html", context)
