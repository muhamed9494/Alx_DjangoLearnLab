from django.contrib import admin
from .models import Tag, Post


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')