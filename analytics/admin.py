from django.contrib import admin
from .models import Analytics
# Register your models here.


@admin.register(Analytics)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', "post_id", "post_clicks", "created")
    list_display_links = ("id", "post_id")
    list_per_page = 30
