from django.contrib import admin
from gallery.models import Author, License, Picture, Thumbnail


admin.site.register(Author)
admin.site.register(License)
admin.site.register(Picture)
admin.site.register(Thumbnail)
