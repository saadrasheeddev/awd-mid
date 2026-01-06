# api/admin.py

from django.contrib import admin
from .models import Wine

@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'quality', 'alcohol', 'pH', 'volatile_acidity')
    list_filter = ('type', 'quality')
    search_fields = ('type',)
    ordering = ('-quality',)