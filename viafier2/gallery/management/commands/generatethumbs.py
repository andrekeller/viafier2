# stdlib
import os
from io import BytesIO

# pyprind
import pyprind

# python image library
from PIL import Image

# django
from django.conf import settings
from django.core.management.base import BaseCommand

# viafier2
from gallery.models import Picture


class ProgressStream:

    def __init__(self, stream):
        self.stream = stream

    def write(self, *args, **kwargs):
        return self.stream.write(ending="", *args, **kwargs)

    def flush(self):
        return self.stream.flush()


class Command(BaseCommand):
    help = 'Generates thumbnails for all pictures in gallery'

    @staticmethod
    def _ensure_thumb_directory(directory):
        os.makedirs(directory, exist_ok=True)
        return directory

    def handle(self, *args, **options):

        queryset = Picture.objects.all()

        progress = pyprind.ProgBar(
            iterations=queryset.count(),
            stream=ProgressStream(self.stdout),
        )

        for picture in Picture.objects.all():
            original_picture = Image.open(BytesIO(picture.picture.read()))
            if original_picture.mode not in ('L', 'RGB'):
                original_picture = original_picture.convert('RGB')
            original_picture_uuid = os.path.splitext(
                os.path.basename(picture.picture.file.name)
            )[0]

            for size in settings.THUMBNAIL_SIZES:
                thumb = original_picture.copy()
                thumb.thumbnail((size, size), Image.ANTIALIAS)
                thumb.save(
                    os.path.join(
                        self._ensure_thumb_directory(
                            os.path.join(
                                settings.MEDIA_ROOT,
                                'gallery', 'thumbs',
                                original_picture_uuid
                            )
                        ),
                        "%d.jpg" % size
                    ),
                    'jpeg',
                    quality=96,
                )

            progress.update()
