from .models import StoreSettings


def store_settings(request):
    """Makes the singleton StoreSettings object, plus top-level categories
    for the navigation bar, available in every template."""
    from products.models import Category

    return {
        "store_settings": StoreSettings.load(),
        "nav_categories": Category.objects.filter(is_active=True, parent__isnull=True).order_by("order", "id"),
    }


def theme(request):
    """Makes the current dark/light theme available in every template."""
    return {"current_theme": getattr(request, "theme", "light")}
