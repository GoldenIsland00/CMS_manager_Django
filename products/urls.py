from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("categories/", views.category_list, name="category_list"),
    path("search/", views.search, name="search"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
]
