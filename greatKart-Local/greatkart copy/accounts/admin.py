from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

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


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html(
            '<img src="{}" width=50, style="border-radius:50%;">'.format(
                object.profile_picture.url
            )
        )

    thumbnail.short_description = "Profile Picture"

    list_display = (
        "thumbnail",
        "user",
        "address_line_1",
        "city",
        "state",
        "city",
        "country",
    )

    search_fields = [
        "user",
        "state",
        "city",
        "address_line_1",
    ]


admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
