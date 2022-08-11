from django.contrib import admin
from .models import *

# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class AdminListing(admin.ModelAdmin):
    list_display = ("id", "title", "description", "price", "user", "imageURL", "category", "openListing")

class AdminBid(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "offer")

class AdminComment(admin.ModelAdmin):
    list_display = ("id", "user", "listing", "comment")

admin.site.register(User, AdminUser)
admin.site.register(Listing, AdminListing)
admin.site.register(Bid, AdminBid)
admin.site.register(Comment, AdminComment)
