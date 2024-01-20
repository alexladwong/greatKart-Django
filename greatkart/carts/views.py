from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from estores.models import Products, Variation
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Create your views here.
def _cart_id(request):  # pipets for backwards
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def Add_to_Cart(request, product_id):
    current_user = request.user
    product = Products.objects.get(id=product_id)  # Get the product

    # If User is Authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value,
                    )
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(
            product=product, user=current_user
        ).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, user=current_user
            )  # Get the user item from the current user session

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # Increase the product variation
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # Update the product variation
                item = CartItem.objects.create(
                    product=product, quantity=1, user=current_user
                )
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()

        # return HttpResponse(cart_item.quantity)
        # exit()

        return redirect("carts")

    # If the user is not logged in(Authenticated)
    else:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value,
                    )
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(
                cart_id=_cart_id(request)
            )  # Get the cart id from the cart session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(
            product=product, cart=cart
        ).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product=product, cart=cart
            )  # Get the cart item from the cart session
            # Existing cart variations -> database
            # Current cart variations -> product_variation
            # item_id -> database

            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)

            if product_variation in ex_var_list:
                # Increase the product variation
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # Update the product variation
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()

        # return HttpResponse(cart_item.quantity)
        # exit()

        return redirect("carts")


# Remove a cart item from the cart session
def Remove_Cart(request, product_id, cart_item_id):
    product = get_object_or_404(Products, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id
            )

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id
            )
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect("carts")


# Delete button a cart item.
def Delete_Cart(request, product_id, cart_item_id):
    product = get_object_or_404(Products, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(
            product=product, user=request.user, id=cart_item_id
        )

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    cart_item.delete()
    return redirect("carts")


# Cart items and logics.


def Carts(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "cart_items": cart_items,
        "quantity": quantity,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "estores/cart.html", context)


# Product Checkout
@login_required(login_url="login")
def Checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "cart_items": cart_items,
        "quantity": quantity,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "estores/checkout.html", context)
