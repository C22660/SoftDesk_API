from django.contrib import admin

# Register your models here.
from authentication.models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    pass