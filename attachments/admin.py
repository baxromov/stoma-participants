from django.contrib import admin
from attachments.models import Attachments


# Register your models here.

@admin.register(Attachments)
class AttachmentsModelAdmin(admin.ModelAdmin):
    pass
