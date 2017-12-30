import os
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


def gallery_pictures_uuid(instance, filename):
    return 'gallery/pictures/%s.jpg' % uuid.uuid1()


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

    @property
    def src(self):
        return '{media_url}gallery/pictures/{uuid}.jpg'.format(
            media_url=settings.MEDIA_URL,
            uuid=str(self),
        )

    @property
    def srcset(self):
        srcset = []
        for size in sorted(settings.THUMBNAIL_SIZES):
            srcset.append(
                '{media_url}gallery/thumbs/{uuid}/{size}.jpg {size}w'.format(
                    media_url=settings.MEDIA_URL,
                    uuid=str(self),
                    size=size,
                )
            )
        return ", ".join(srcset)
