from django.contrib import admin
from .models import *

# import admin_thumbnails


# @admin_thumbnails.thumbnails("image")
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "product_name",
        "price",
        "stock",
        "category",
        "modified_date",
        "is_available",
    )
    prepopulated_fields = {"slug": ("product_name",)}
    inlines = [ProductGalleryInline]


class VariationAdmin(admin.ModelAdmin):
    search_fields = ["variation_category", "product"]
    list_display = (
        "product",
        "variation_category",
        "variation_value",
        "is_active",
    )
    list_editable = ("is_active",)
    list_filter = (
        "product",
        "variation_category",
        "variation_value",
    )


admin.site.register(Products, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
