from django.contrib import admin
from .models import Artist, ArtistClaimed, ArtistLink, Subscription

class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Artist, ArtistAdmin)
admin.site.register(ArtistClaimed)
admin.site.register(ArtistLink)
admin.site.register(Subscription)

# Register your models here.
