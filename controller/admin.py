from django.contrib import admin
from .models import Blog, Contact
# Register your models here.


@admin.register(Blog)
class BlogPostAdmin(admin.ModelAdmin):
    exclude = ['slug', 'analytics']
    list_display = ('_id', 'title', 'created', 'updated',)
    list_display_links = ('_id', 'title')
    list_per_page = 30


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('_id', "username", "created")
    list_display_links = ("_id", "username")
    list_per_page = 30
