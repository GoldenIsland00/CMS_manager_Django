from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name_fa = models.CharField(_("Name (Persian)"), max_length=150)
    name_en = models.CharField(_("Name (English)"), max_length=150)
    slug = models.SlugField(_("Slug"), max_length=170, unique=True, allow_unicode=True)

    description_fa = models.TextField(_("Description (Persian)"), blank=True)
    description_en = models.TextField(_("Description (English)"), blank=True)

    image = models.ImageField(_("Image"), upload_to="categories/", blank=True, null=True)
    parent = models.ForeignKey(
        "self", verbose_name=_("Parent category"), null=True, blank=True,
        related_name="children", on_delete=models.SET_NULL,
    )
    order = models.PositiveIntegerField(_("Display order"), default=0)
    is_active = models.BooleanField(_("Active"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["order", "name_en"]

    def __str__(self):
        return f"{self.name_fa} / {self.name_en}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en or self.name_fa, allow_unicode=True)
        super().save(*args, **kwargs)

    @property
    def name(self):
        return self.name_fa if get_language() == "fa" else self.name_en

    @property
    def description(self):
        return self.description_fa if get_language() == "fa" else self.description_en

    def get_absolute_url(self):
        return reverse("products:category_detail", kwargs={"slug": self.slug})

    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()


class Product(models.Model):
    category = models.ForeignKey(
        Category, verbose_name=_("Category"), related_name="products", on_delete=models.CASCADE,
    )
    name_fa = models.CharField(_("Name (Persian)"), max_length=200)
    name_en = models.CharField(_("Name (English)"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=220, unique=True, allow_unicode=True)

    sku = models.CharField(_("SKU / product code"), max_length=50, blank=True)

    short_description_fa = models.CharField(_("Short description (Persian)"), max_length=300, blank=True)
    short_description_en = models.CharField(_("Short description (English)"), max_length=300, blank=True)

    description_fa = models.TextField(_("Full description (Persian)"), blank=True)
    description_en = models.TextField(_("Full description (English)"), blank=True)

    price = models.DecimalField(_("Price"), max_digits=12, decimal_places=0, help_text=_("Price in Toman"))
    discount_price = models.DecimalField(
        _("Discount price"), max_digits=12, decimal_places=0, blank=True, null=True,
        help_text=_("Leave empty if the product has no discount."),
    )

    stock = models.PositiveIntegerField(_("Stock quantity"), default=0)
    is_active = models.BooleanField(_("Active / visible on site"), default=True)
    is_featured = models.BooleanField(_("Featured"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name_fa} / {self.name_en}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en or self.name_fa, allow_unicode=True)
        super().save(*args, **kwargs)

    # ---- bilingual helpers -------------------------------------------------
    @property
    def name(self):
        return self.name_fa if get_language() == "fa" else self.name_en

    @property
    def short_description(self):
        return self.short_description_fa if get_language() == "fa" else self.short_description_en

    @property
    def description(self):
        return self.description_fa if get_language() == "fa" else self.description_en

    # ---- pricing helpers ----------------------------------------------------
    @property
    def has_discount(self):
        return bool(self.discount_price) and self.discount_price < self.price

    @property
    def final_price(self):
        return self.discount_price if self.has_discount else self.price

    @property
    def discount_percent(self):
        if not self.has_discount:
            return 0
        return round((1 - (self.discount_price / self.price)) * 100)

    @property
    def in_stock(self):
        return self.stock > 0

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"slug": self.slug})

    @property
    def main_image(self):
        img = self.images.filter(is_main=True).first()
        return img or self.images.first()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to="products/%Y/%m/")
    alt_text = models.CharField(_("Alt text"), max_length=200, blank=True)
    is_main = models.BooleanField(_("Main image"), default=False)
    order = models.PositiveIntegerField(_("Display order"), default=0)

    class Meta:
        verbose_name = _("Product image")
        verbose_name_plural = _("Product images")
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.product} - image {self.pk}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_main:
            # only one main image per product
            ProductImage.objects.filter(product=self.product).exclude(pk=self.pk).update(is_main=False)


class ProductSpecification(models.Model):
    """Key/value technical specification row shown in the product detail table."""

    product = models.ForeignKey(Product, related_name="specifications", on_delete=models.CASCADE)
    title_fa = models.CharField(_("Title (Persian)"), max_length=100)
    title_en = models.CharField(_("Title (English)"), max_length=100)
    value_fa = models.CharField(_("Value (Persian)"), max_length=250)
    value_en = models.CharField(_("Value (English)"), max_length=250)
    order = models.PositiveIntegerField(_("Display order"), default=0)

    class Meta:
        verbose_name = _("Specification")
        verbose_name_plural = _("Specifications")
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.title_fa}: {self.value_fa}"

    @property
    def title(self):
        return self.title_fa if get_language() == "fa" else self.title_en

    @property
    def value(self):
        return self.value_fa if get_language() == "fa" else self.value_en
