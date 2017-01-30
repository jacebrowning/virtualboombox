from django.contrib import admin
from .models import Account, Song


admin.site.site_title = "Virtual Boombox Admin"
admin.site.site_header = "Virtual Boombox"


class ClickableMixin:

    def clickable_url(self, obj):
        return f'<a href="{obj.url}">{obj.url}</a>'

    clickable_url.allow_tags = True
    clickable_url.short_description = 'Location'


class AccountAdmin(admin.ModelAdmin, ClickableMixin):
    list_display = [
        'username',
        'clickable_url',
    ]


class SongAdmin(admin.ModelAdmin, ClickableMixin):
    list_display = [
        'name',
        'username',
        'clickable_url',
        'date',
    ]

    def username(self, obj):
        return obj.account.username if obj.account else ""

    username.short_description = 'Account'


admin.site.register(Account, AccountAdmin)
admin.site.register(Song, SongAdmin)
