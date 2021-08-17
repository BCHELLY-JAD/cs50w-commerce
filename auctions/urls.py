from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("item/<int:item_id>", views.item, name="item"),
    path("item/comment/<int:item_id>", views.addComment, name="add"),
    path("categories", views.Categories, name="categories"),
    path("categories/<str:name>", views.this_category, name="this_category"),
    path("item/added/<int:item_id>", views.addwatchlist, name="addwatchlist"),
    path("item/removed/<int:item_id>", views.removewatchlist, name="removewatchlist"),
    path("watchlist", views.watch_list, name="watchlist"),
    path("closed/<int:item_id>", views.closelisting, name="close")
    
]