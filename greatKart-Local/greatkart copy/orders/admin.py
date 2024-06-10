from django.contrib import admin
from .models import *


# Register your models here.
class orderProductsInline(admin.TabularInline):
    model = orderProducts
    
    readonly_fields = (
        "variation",
        "payment",
        "user",
        "product",
        "quantity",
        "product_price",
        "ordered",
    )
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "full_name",
        "phone_number",
        "email",
        "city",
        "address_line_1",
        "order_total",
        "tax",
        "status",
        "is_ordered",
        "created_at",
    ]
    list_filter = ["status", "is_ordered", "created_at"]
    search_fields = [
        "order_number",
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "address_line_1",
    ]
    list_per_page = 20
    inlines = [orderProductsInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(orderProducts)
