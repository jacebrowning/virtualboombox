from django.contrib import admin
from .models import Song


admin.site.site_title = "Virtual BoomBox Admin"
admin.site.site_header = "Virtual BoomBox"

admin.site.register(Song)
