from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render

from orders.models import orderProducts

from .forms import ReviewForm
from .models import *
from store.models import *
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages, auth
from django.db.models import Q


# Create your views here.


def estores(request, category_slug=None):
    category = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Products.objects.filter(
            category=categories, is_available=True
        ).order_by("id")
        paginator = Paginator(products, 3)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Products.objects.all().filter(is_available=True).order_by("id")
        paginator = Paginator(products, 6)
        page = request.GET.get("page")
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        # "products": products,
        "product_count": product_count,
        "products": paged_products,
    }
    return render(request, "estores/estores.html", context)


def Product_Details(request, category_slug, product_slug):
    try:
        single_product = Products.objects.get(
            category__slug=category_slug, slug=product_slug
        )
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request), product=single_product
        ).exists()
        # return HttpResponse(in_cart)
        # exit()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = orderProducts.objects.filter(
                user=request.user, product_id=single_product.id
            ).exists()

        except orderProducts.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Fetch the Product Reviews and the stars
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    # Get Product Gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        "single_product": single_product,
        "in_cart": in_cart,
        "orderproduct": orderproduct,
        "reviews": reviews,
        "product_gallery": product_gallery,
    }
    return render(request, "estores/product_details.html", context)


def Search(request):
    if "keyword" in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = Products.objects.order_by("-created_date").filter(
                Q(descriptions__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            product_count = products.count()
    context = {
        "products": products,
        "product_count": product_count,
    }
    return render(request, "estores/estores.html", context)


# Customer_Review
def CustomerReview(request, product_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id
            )
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(
                request,
                f"Thank you { request.user.first_name }! Your Review has been Updated successfully!",
            )
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(
                    request,
                    f"Thank you { request.user.first_name }! Your Review is Submitted successfully!",
                )
            return redirect(url)
