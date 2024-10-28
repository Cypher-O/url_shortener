from django.contrib import admin

# urlshortener/apps/shortener/admin.py

from django.contrib import admin
from .models import URL

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'shortened_url')