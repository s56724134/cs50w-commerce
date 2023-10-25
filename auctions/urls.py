from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-listing", views.create_listing, name="create_listing"),
    path("display-category", views.display_category, name="display_category"),
    path("Listing/<str:pk>", views.listing, name="listing"),
    path("removeWatchlist/<str:pk>", views.removeWatchlist, name="removeWatchlist"),
    path("addWatchlist/<str:pk>", views.addWatchlist, name="addWatchlist"),
    path("watchlist", views.displayWatchlist, name="watchlist"),
    path("addReview/<str:pk>", views.addReview, name="addReview"),
    path("addBid/<str:pk>", views.addBid, name="addBid"),
    path("closeAuction/<str:pk>", views.closeAuction, name="closeAuction"),
]
