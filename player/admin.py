from django.contrib import admin
from .models import Song


admin.site.site_title = "Virtual Boombox Admin"
admin.site.site_header = "Virtual Boombox"

admin.site.register(Song)
