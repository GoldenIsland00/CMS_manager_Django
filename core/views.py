from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import url_has_allowed_host_and_scheme

from products.models import Category, Product

from .middleware import DEFAULT_THEME, THEME_COOKIE_NAME, VALID_THEMES


def home(request):
    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by("order", "id")
    featured_products = (
        Product.objects.filter(is_active=True, is_featured=True)
        .select_related("category")
        .prefetch_related("images")[:8]
    )
    latest_products = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related("images")
        .order_by("-created_at")[:8]
    )
    return render(
        request,
        "core/home.html",
        {
            "categories": categories,
            "featured_products": featured_products,
            "latest_products": latest_products,
        },
    )


def toggle_theme(request):
    """
    Flips the visitor's theme cookie between light/dark and redirects
    back to the page they came from.
    """
    next_url = request.POST.get("next") or request.GET.get("next") or "/"
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/"

    current = getattr(request, "theme", DEFAULT_THEME)
    new_theme = "dark" if current == "light" else "light"
    if new_theme not in VALID_THEMES:
        new_theme = DEFAULT_THEME

    response = HttpResponseRedirect(next_url)
    response.set_cookie(THEME_COOKIE_NAME, new_theme, max_age=60 * 60 * 24 * 365)
    return response
