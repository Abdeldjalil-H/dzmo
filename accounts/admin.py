from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm
# Register your models here.

from .models import StudentProgress
User = get_user_model()

class ProgressInline(admin.StackedInline):
    model = StudentProgress

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    inlines = [ProgressInline]
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('first_name','last_name','email',)
    list_filter = ('is_admin','is_staff','is_active','grade')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('المعلومات الشخصية', {'fields': ('first_name','last_name','date_of_birth','wilaya','grade','sex',)}),
        ('التخويلات', {'fields': ('is_admin','is_staff','is_active', 'is_corrector')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','first_name','last_name')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
