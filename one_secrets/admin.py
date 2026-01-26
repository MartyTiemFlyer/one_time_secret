from django.contrib import admin

# Register your models here.
from one_secrets.models import Secret
admin.site.register(Secret)