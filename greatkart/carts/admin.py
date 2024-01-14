from django.contrib import admin
from .models import *


# Register your models here.
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "cart",
        "quantity",
        "is_active",
    )


class CartAdmin(admin.ModelAdmin):
    list_display = (
        "cart_id",
        "date_added",
    )


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart, CartAdmin)

search_fields = ["cart", "product"]
