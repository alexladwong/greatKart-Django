from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from estores.models import Products
from .models import Cart, CartItem


# Create your views here.
def _card_id(request):  # pipets for backwards
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def Add_to_Cart(request, product_id):
    product = Products.objects.get(id=product_id)  # Get the product
    try:
        cart = Cart.objects.get(
            cart_id=_card_id(request)
        )  # Get the cart id from the cart session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_card_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart
        )  # Get the cart item from the cart session
        cart_item.quantity += 1  # Get the quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()

    # return HttpResponse(cart_item.quantity)
    # exit()

    return redirect("carts")


# Remove a cart item from the cart session
def Remove_Cart(request, product_id):
    cart = Cart.objects.get(cart_id=_card_id(request))
    product = get_object_or_404(Products, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("carts")


# Delete button a cart item.
def Delete_Cart(request, product_id):
    cart = Cart.objects.get(cart_id=_card_id(request))
    product = get_object_or_404(Products, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    return redirect("carts")


# Cart items and logics.
def Carts(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_card_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectNotExist:
        pass

    context = {
        "total": total,
        "cart_items": cart_items,
        "quantity": quantity,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "estores/cart.html", context)
