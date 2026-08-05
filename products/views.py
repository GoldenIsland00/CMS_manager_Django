from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def category_list(request):
    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by("order", "id")
    return render(request, "products/category_list.html", {"categories": categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = (
        Product.objects.filter(category=category, is_active=True)
        .select_related("category")
        .prefetch_related("images")
        .order_by("-created_at")
    )

    sort = request.GET.get("sort")
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-created_at")

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by("order", "id")

    return render(
        request,
        "products/category_list.html",
        {
            "categories": categories,
            "active_category": category,
            "page_obj": page_obj,
            "products": page_obj.object_list,
            "sort": sort,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("images", "specifications"),
        slug=slug,
        is_active=True,
    )
    related_products = (
        Product.objects.filter(category=product.category, is_active=True)
        .exclude(pk=product.pk)
        .prefetch_related("images")[:4]
    )
    return render(
        request,
        "products/product_detail.html",
        {"product": product, "related_products": related_products},
    )


def search(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.none()
    if query:
        products = (
            Product.objects.filter(is_active=True)
            .filter(
                Q(name_fa__icontains=query)
                | Q(name_en__icontains=query)
                | Q(sku__icontains=query)
                | Q(short_description_fa__icontains=query)
                | Q(short_description_en__icontains=query)
            )
            .select_related("category")
            .prefetch_related("images")
            .distinct()
        )

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by("order", "id")

    return render(
        request,
        "products/category_list.html",
        {
            "categories": categories,
            "page_obj": page_obj,
            "products": page_obj.object_list,
            "search_query": query,
        },
    )
