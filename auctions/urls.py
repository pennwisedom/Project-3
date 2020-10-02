from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:list_id>", views.listing, name="listing"),
    path("new", views.create, name="create"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_detail, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<str:list_id>", views.watchlist, name="watchlist")
]
