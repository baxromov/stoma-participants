from django.contrib import admin
from django.utils.html import format_html

from participant.models import Participant


# Register your models here.

@admin.register(Participant)
class CountryModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'first_name',
        'last_name',
        'phone',
        'country',
        'instagram_username'
    ]
    list_display_links = [
        'id',
        'first_name',
        'last_name'
    ]
    search_fields = [
        'first_name',
        'last_name',
        'country',
        'instagram_username'
    ]
    readonly_fields = ['show_firm_url']

    def show_firm_url(self, obj):
        return format_html(f"{obj.file[0]}<a href='1'></a>")
