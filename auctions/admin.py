from django.contrib import admin
from .models import *

# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = ("id", "username", "email")

admin.site.register(User, AdminUser)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
