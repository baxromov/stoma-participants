from django.contrib import admin
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
