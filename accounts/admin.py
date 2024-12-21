from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import Corrector, Team

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ("first_name", "last_name", "email")
    list_filter = ("is_admin", "is_staff", "is_active", "grade", "team")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "المعلومات الشخصية",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "wilaya",
                    "grade",
                    "sex",
                )
            },
        ),
        (
            "التخويلات",
            {"fields": ("is_admin", "is_staff", "is_active", "is_corrector")},
        ),
        ("الفريق", {"fields": ("team",)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Team)
admin.site.register(Corrector)
