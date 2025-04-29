from django.contrib import admin
from .models import Link

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'link_type', 'created_at')
    list_filter = ('link_type', 'owner')
    search_fields = ('title', 'url')
    readonly_fields = ('created_at', 'updated_at')