from django.contrib import admin
from gallery.models import Author, License, Picture, Thumbnail, Vector


admin.site.register(Author)
admin.site.register(License)
admin.site.register(Picture)
admin.site.register(Thumbnail)
admin.site.register(Vector)
