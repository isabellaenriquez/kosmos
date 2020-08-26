from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('products', views.products, name="products"),
    path('view_product/<int:product_id>', views.view_product, name="view_product"),
    path('search', views.search, name="search"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),
    path('my_makeup_bag', views.my_bag, name="bag"),
    path('my_collections', views.my_collections, name="my_collections"),
    path('public_collections', views.public_collections, name="public_collections"),
    path('curate', views.curate, name="curate"),
    path('view_collection/<int:collect_id>', views.view_collection, name="view_collection"),
    path('review', views.review, name="review"),
    path('profile/@<str:username>', views.profile, name="profile"),
    path('mailbox', views.mailbox, name="mailbox")
]