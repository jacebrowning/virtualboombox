from django.contrib import admin

from .models import Reaction


class ReactionAdmin(admin.ModelAdmin):
    list_display = [
        'song',
        'comment',
        'date',
    ]
    ordering = ['-date']


admin.site.register(Reaction, ReactionAdmin)
