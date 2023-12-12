from django.contrib import admin
from .models import *

class BannerAdmin(admin.ModelAdmin):
    list_display = ('alt_text', 'image_tag_path')

admin.site.register(Banner, BannerAdmin)