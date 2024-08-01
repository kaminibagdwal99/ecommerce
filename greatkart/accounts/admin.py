from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


class AccountAdmin(UserAdmin):
    list_display = (
        'first_name', 'last_name','username','email','is_active','date_joined', 'last_login'
        )
    list_display_links =('first_name', 'last_name','username','email')
    readonly_fields =('date_joined', 'last_login')
    ordering=('-date_joined',)
    filter_horizontal =()
    list_filter = ()
    fieldsets = ()
admin.site.register(Account, AccountAdmin)

# Register your models here.
