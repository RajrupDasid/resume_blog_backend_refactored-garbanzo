from django.contrib import admin
from .models import Blog
# Register your models here.


@admin.register(Blog)
class BlogPostAdmin(admin.ModelAdmin):
    exclude = ['slug',]
    list_display = ('_id', 'title', 'created', 'updated',)
    list_display_links = ('_id', 'title')
    list_per_page = 30
