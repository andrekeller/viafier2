import os
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image
from io import BytesIO


def gallery_pictures_uuid(instance, filename):
    return 'gallery/pictures/%s.jpg' % uuid.uuid1()

def gallery_thumbs_uuid(instance, filename):
    return 'gallery/thumbs/{}/{}.jpg'.format(filename, instance.size)


class Author(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        # translation
        verbose_name=_('author')
    )
    affiliation = models.CharField(
        blank=True,
        max_length=255,
        null=True,
        # translation
        verbose_name=_('affiliation'),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    def __str__(self):
        if self.affiliation:
            return "%s (%s)" % (self.name, self.affiliation)
        else:
            return "%s" % self.name


class License(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        # translation
        verbose_name=_('license name'),
    )
    url = models.URLField(
        # translation
        verbose_name=_('url'),
        help_text=_('url to license text'),
    )

    class Meta:
        ordering = ('name'),
        verbose_name = _('license')
        verbose_name_plural = _('licenses')

    def __str__(self):
        return "%s" % self.name


class Thumbnail(models.Model):
    picture = models.ForeignKey(
        on_delete=models.CASCADE,
        to='gallery.Picture',
        verbose_name=_('picture'),
        related_name='thumbnails',
    )
    thumbnail = models.ImageField(
        upload_to=gallery_thumbs_uuid,
        verbose_name=_('thumbnail'),
    )
    size = models.IntegerField(
        verbose_name=_('size')
    )

    class Meta:
        verbose_name = _('thumbnail')
        verbose_name_plural = _('thumbnails')


class Picture(models.Model):
    author = models.ForeignKey(
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        to='gallery.Author',
        # translation
        verbose_name=_('author'),
    )
    license = models.ForeignKey(
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        to='gallery.License',
        # translation
        verbose_name=_('license'),
    )
    source = models.URLField(
        blank=True,
        null=True,
        # translation
        help_text=_('link to original picture'),
        verbose_name=_('source'),
    )
    picture = models.ImageField(
        upload_to=gallery_pictures_uuid,
        # translation
        verbose_name=_('picture'),
    )

    class Meta:
        verbose_name = _('picture')
        verbose_name_plural = _('pictures')

    def __str__(self):
        if self.picture:
            return os.path.splitext(os.path.basename(self.picture.file.name))[0]
        else:
            return super().__str__()

    def save(self, **kwargs):
        super().save(**kwargs)
        original = Image.open(BytesIO(self.picture.read()))
        if original.mode not in ('L', 'RGB'):
            original = original.convert('RGB')
        for size in settings.THUMBNAIL_SIZES:
            thumb = original.copy()
            thumb.thumbnail((size, size), Image.ANTIALIAS)

            thumb_memorybuffer = BytesIO()
            thumb.save(thumb_memorybuffer, 'jpeg', quality=96)
            thumb_memorybuffer.seek(0)

            thumbnail_uploaded_file = SimpleUploadedFile(
                name=self.picture.name.rsplit('.')[0],
                content=thumb_memorybuffer.read(),
                content_type='image/jpeg',
            )
            Thumbnail.objects.get_or_create(
                picture=self,
                size=size,
                defaults={'thumbnail': thumbnail_uploaded_file},
            )
            thumb_memorybuffer.close()

    @property
    def src(self):
        return self.picture.url

    @property
    def srcset(self):
        srcset = []
        for thumbnail in self.thumbnails.all():
            srcset.append('{url} {size}w'.format(
                url=thumbnail.thumbnail.url,
                size=thumbnail.size)
            )
        return ", ".join(srcset)
