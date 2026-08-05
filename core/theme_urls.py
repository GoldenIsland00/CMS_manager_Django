from django.urls import path

from . import views

urlpatterns = [
    path("", views.toggle_theme, name="toggle_theme"),
]
