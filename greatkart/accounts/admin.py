from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.
class AccountAdmin(UserAdmin):
    search_fields = [
        "username",
        "last_name",
        "first_name",
    ]
    list_display = (
        "email",
        "username",
        "date_joined",
        "first_name",
        "last_name",
        "last_login",
        "is_active",
    )
    list_display_links = ("email", "username", "date_joined", "last_name")
    readonly_fields = ("email", "date_joined", "last_login")
    ordering = ("-date_joined", "-last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
