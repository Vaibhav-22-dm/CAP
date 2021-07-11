from django.contrib import admin
from AbstractUserModel.models import MyUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# Register your models here.
class MyUserAdmin(BaseUserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'last_login', 'is_admin', 'is_active',)
    search_fields = ('email', 'first_name',)
    readonly_fields = ('last_login',)
    filter_horizontal = ()
    list_filter = ('last_login',)
    fieldsets = ()

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'first_name', 'middle_name', 'last_name', 'password1','password2'),


        }),
    )

    ordering = ('email',)

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Customer)