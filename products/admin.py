from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Category, Product, ProductImage, ProductSpecification


# ---------------------------------------------------------------------------
# Multiple-file upload widget/field
# Lets the admin select and upload several product photos in ONE click,
# from the product's own add/change page - no need to save first.
# ---------------------------------------------------------------------------
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {"multiple": True}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, "getlist"):
            upload = files.getlist(name)
        else:
            upload = files.get(name)
        return upload or None


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if data is None:
            return []
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)


class ProductAdminForm(forms.ModelForm):
    extra_images = MultipleFileField(
        required=False,
        label=_("Upload images"),
        help_text=_("Select several photos at once (Ctrl/Cmd + click). The first one becomes the main image if the product has none yet."),
    )

    class Meta:
        model = Product
        fields = "__all__"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    fields = ("preview", "image", "alt_text", "is_main", "order")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj and obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;" />', obj.image.url)
        return "—"
    preview.short_description = _("Preview")


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    fields = ("title_fa", "title_en", "value_fa", "value_en", "order")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_fa", "name_en", "parent", "product_count", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name_fa", "name_en")
    prepopulated_fields = {"slug": ("name_en",)}
    list_filter = ("is_active", "parent")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [ProductImageInline, ProductSpecificationInline]

    list_display = ("thumb", "name_fa", "name_en", "category", "price", "discount_price", "stock", "is_active", "is_featured")
    list_editable = ("is_active", "is_featured")
    list_filter = ("category", "is_active", "is_featured")
    search_fields = ("name_fa", "name_en", "sku")
    prepopulated_fields = {"slug": ("name_en",)}

    fieldsets = (
        (_("Category"), {"fields": ("category",)}),
        (_("Names & slug"), {"fields": ("name_fa", "name_en", "slug", "sku")}),
        (_("Short description"), {"fields": ("short_description_fa", "short_description_en")}),
        (_("Full description"), {"fields": ("description_fa", "description_en")}),
        (_("Pricing & stock"), {"fields": ("price", "discount_price", "stock")}),
        (_("Visibility"), {"fields": ("is_active", "is_featured")}),
        (_("Photos"), {"fields": ("extra_images",)}),
    )

    def thumb(self, obj):
        img = obj.main_image
        if img:
            return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', img.image.url)
        return "—"
    thumb.short_description = _("Photo")

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        files = form.cleaned_data.get("extra_images") or []
        if not files:
            return
        existing_count = form.instance.images.count()
        for i, f in enumerate(files):
            ProductImage.objects.create(
                product=form.instance,
                image=f,
                is_main=(existing_count == 0 and i == 0),
                order=existing_count + i,
            )
