from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.form import UserRegistrationForm
from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserRegistrationForm

    list_display = ("email", "is_staff", "is_active")
    search_fields = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {
            "fields": ("email", "password"),
        }),
        ("Профиль", {
            "fields": ("avatar", "mobile_number", "country"),
        }),
        ("Права доступа", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "avatar",
                "mobile_number",
                "country",
            ),
        }),
    )