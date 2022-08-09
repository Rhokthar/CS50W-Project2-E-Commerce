from django.contrib import admin
from .models import *

# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class AdminListing(admin.ModelAdmin):
    list_display = ("id", "title", "price", "user")

admin.site.register(User, AdminUser)
admin.site.register(Listing, AdminListing)
admin.site.register(Bid)
admin.site.register(Comment)
