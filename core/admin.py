from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import StoreSettings


@admin.register(StoreSettings)
class StoreSettingsAdmin(admin.ModelAdmin):
    """
    Since this is a singleton, disable 'add' once a row exists and disable 'delete'.
    """

    readonly_fields = ("qr_preview", "updated_at")
    fieldsets = (
        (_("Store identity"), {
            "fields": ("store_name_fa", "store_name_en", "slogan_fa", "slogan_en", "logo")
        }),
        (_("Contact"), {
            "fields": ("store_url", "phone", "address_fa", "address_en", "instagram", "telegram", "whatsapp")
        }),
        (_("QR code"), {
            "fields": ("qr_preview", "qr_code"),
            "description": _("The QR code is generated automatically from the Store URL above whenever you save."),
        }),
    )

    def qr_preview(self, obj):
        if obj and obj.qr_code:
            return format_html('<img src="{}" style="width:160px;height:160px;border:1px solid #ddd;padding:6px;" />', obj.qr_code.url)
        return _("QR code will appear here after you save.")
    qr_preview.short_description = _("Current QR code")

    def has_add_permission(self, request):
        return not StoreSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        # Redirect straight to the single settings object instead of showing a list
        obj = StoreSettings.load()
        from django.shortcuts import redirect
        return redirect("admin:core_storesettings_change", obj.pk)
