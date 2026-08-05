import io
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop_cms.settings")
django.setup()

from django.core.files.base import ContentFile
from PIL import Image

from core.models import StoreSettings
from products.models import Category, Product, ProductImage, ProductSpecification

settings_obj = StoreSettings.load()
settings_obj.store_name_fa = "قشم کلین دمو"
settings_obj.store_name_en = "Qeshm Clean Demo"
settings_obj.slogan_fa = "محصولات شوینده و بهداشتی با کیفیت"
settings_obj.slogan_en = "Quality cleaning & hygiene products"
settings_obj.store_url = "https://example.com"
settings_obj.phone = "09120000000"
settings_obj.save()

cat, _ = Category.objects.get_or_create(
    slug="washing", defaults=dict(name_fa="لباسشویی", name_en="Laundry")
)

def dummy_image(color, name):
    img = Image.new("RGB", (400, 400), color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return ContentFile(buf.getvalue(), name=name)


product, created = Product.objects.get_or_create(
    slug="ariel-pods",
    defaults=dict(
        category=cat,
        name_fa="اریل کول کلین قرص لباسشویی",
        name_en="Ariel Pods Cool Clean",
        short_description_fa="قرص لباسشویی سه‌کاره با رایحه فرانسوی",
        short_description_en="3-in-1 laundry pods, French scent",
        description_fa="این محصول شامل ۳۹ عدد قرص لباسشویی است که لکه‌ها را به‌خوبی پاک می‌کند.",
        description_en="Contains 39 laundry pods that remove tough stains effectively.",
        price=850000,
        discount_price=690000,
        stock=25,
        is_active=True,
        is_featured=True,
        sku="AR-149",
    ),
)

if created:
    ProductImage.objects.create(product=product, image=dummy_image("orange", "p1.jpg"), is_main=True, order=0)
    ProductImage.objects.create(product=product, image=dummy_image("blue", "p2.jpg"), order=1)
    ProductSpecification.objects.create(product=product, title_fa="وزن", title_en="Weight", value_fa="1.02 کیلوگرم", value_en="1.02 kg", order=0)
    ProductSpecification.objects.create(product=product, title_fa="تعداد", title_en="Count", value_fa="39 عدد", value_en="39 pcs", order=1)
    ProductSpecification.objects.create(product=product, title_fa="کشور سازنده", title_en="Made in", value_fa="فرانسه", value_en="France", order=2)

print("Seed complete. Product URL slug:", product.slug)
