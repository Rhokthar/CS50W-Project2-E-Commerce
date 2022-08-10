from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.CreateListing, name="create-listing"),
    path("listings/<int:id>", views.ListingsPage, name="listing-page"),
    path("watchlist", views.WatchlistHandler, name="watchlist"),
    path("bid", views.NewBid, name="bid"),
    path("close-listing", views.CloseListing, name="close-listing")
]
