from django.contrib import admin
from one_secrets.models import Secret


# Register your models here.

@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    """Секрет — иммутабельный, после создания его нельзя менять даже из админки"""

    list_display = ("uuid",)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # объект уже существует --> change view
            return ("secret",)
        return ()
