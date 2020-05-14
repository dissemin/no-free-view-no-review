from django.contrib import admin
from .models import Signatory

class SignatoryAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)

admin.site.register(Signatory, SignatoryAdmin)
