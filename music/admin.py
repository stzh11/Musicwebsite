from django.contrib import admin
from .models import Album, Song, Genre, AlbumGenre, SongGenre, AlbumConnection, SongConnection, SongLike, AlbumLike


class SongAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}

class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title", )}

admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Genre)
admin.site.register(AlbumGenre)
admin.site.register(SongGenre)
admin.site.register(AlbumConnection)    
admin.site.register(SongConnection)
admin.site.register(SongLike)
admin.site.register(AlbumLike)
# Register your models here.
