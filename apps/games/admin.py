from django.contrib import admin

from apps.games.infra.models import Game, Genre, LibraryEntry

admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(LibraryEntry)
