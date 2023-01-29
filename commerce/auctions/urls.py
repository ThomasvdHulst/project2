from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.view_listing, name="view_listing"),
    path("listings/<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("listings/createlisting", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>/place_comment", views.place_comment, name="place_comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_name>", views.view_category, name="view_category"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("manage_watchlist/<int:listing_id>", views.manage_watchlist, name="manage_watchlist"),
    path("listings/closelisting/<int:listing_id>", views.close_listing, name="close_listing"),
    path("listings/your_listings", views.your_listings, name="your_listings"),
    path("your_wins", views.your_wins, name="your_wins")
]
