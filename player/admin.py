from django.contrib import admin
from .models import Account, Song


admin.site.site_title = "Virtual Boombox Admin"
admin.site.site_header = "Virtual Boombox"


class ClickableMixin:

    def clickable_lastfm_url(self, obj):
        return f'<a href="{obj.lastfm_url}">{obj.lastfm_url}</a>'

    clickable_lastfm_url.allow_tags = True
    clickable_lastfm_url.short_description = 'Last.fm'

    def clickable_maps_url(self, obj):
        return f'<a href="{obj.maps_url}">{obj.maps_url}</a>'

    clickable_maps_url.allow_tags = True
    clickable_maps_url.short_description = 'Location'


class AccountAdmin(admin.ModelAdmin, ClickableMixin):
    list_display = [
        'username',
        'clickable_maps_url',
        'date',
    ]
    ordering = ['-date']


class SongAdmin(admin.ModelAdmin, ClickableMixin):
    list_display = [
        'name',
        'clickable_lastfm_url',
        'username',
        'clickable_maps_url',
        'date',
    ]
    ordering = ['-date']

    def username(self, obj):
        return obj.account.username if obj.account else ""

    username.short_description = 'Account'


admin.site.register(Account, AccountAdmin)
admin.site.register(Song, SongAdmin)
