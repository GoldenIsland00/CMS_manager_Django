import io

import qrcode
from django.core.files.base import ContentFile
from django.db import models
from django.utils.translation import gettext_lazy as _


class StoreSettings(models.Model):
    """
    Singleton model holding the store's general/bilingual info.
    Only one row is ever allowed - manage it from the admin panel.
    A QR code pointing at `store_url` is (re)generated automatically
    whenever the URL changes.
    """

    store_name_fa = models.CharField(_("Store name (Persian)"), max_length=150, default="فروشگاه من")
    store_name_en = models.CharField(_("Store name (English)"), max_length=150, default="My Store")

    slogan_fa = models.CharField(_("Slogan (Persian)"), max_length=250, blank=True)
    slogan_en = models.CharField(_("Slogan (English)"), max_length=250, blank=True)

    logo = models.ImageField(_("Logo"), upload_to="store/", blank=True, null=True)

    store_url = models.URLField(
        _("Store URL"),
        help_text=_("Public URL of the store - this is what the QR code will point to."),
        default="https://example.com",
    )
    phone = models.CharField(_("Phone number"), max_length=30, blank=True)
    address_fa = models.CharField(_("Address (Persian)"), max_length=300, blank=True)
    address_en = models.CharField(_("Address (English)"), max_length=300, blank=True)
    instagram = models.URLField(_("Instagram URL"), blank=True)
    telegram = models.URLField(_("Telegram URL"), blank=True)
    whatsapp = models.URLField(_("WhatsApp URL"), blank=True)

    qr_code = models.ImageField(_("QR code (auto-generated)"), upload_to="store/qr/", blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Store settings")
        verbose_name_plural = _("Store settings")

    def __str__(self):
        return self.store_name_en or self.store_name_fa or "Store settings"

    def save(self, *args, **kwargs):
        # Enforce a single row (id = 1)
        self.pk = 1
        self._generate_qr_code()
        super().save(*args, **kwargs)

    def _generate_qr_code(self):
        """(Re)build the QR code image whenever store_url changes."""
        old = StoreSettings.objects.filter(pk=1).first()
        if old and old.store_url == self.store_url and old.qr_code:
            # nothing changed, keep existing file
            self.qr_code = old.qr_code
            return

        qr = qrcode.QRCode(box_size=10, border=2)
        qr.add_data(self.store_url or "")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        file_name = "store-qr.png"
        self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

    @classmethod
    def load(cls):
        obj, _created = cls.objects.get_or_create(pk=1)
        return obj
