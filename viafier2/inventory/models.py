from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from taggit_selectize.managers import TaggableManager


class ArticleManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            status__in=[0, 1]
        ).select_related(
            'manufacturer',
            'vendor'
        )


class Article(models.Model):
    BOUGHT_STATUS = 0
    ORDERED_STATUS = 1
    SOLD_STATUS = 2
    DISPOSED_STATUS = 3
    DESIRED_STATUS = 3

    STATUS_CHOICES = (
        (BOUGHT_STATUS, _('bought')),
        (ORDERED_STATUS, _('ordered')),
        (SOLD_STATUS, _('sold')),
        (DISPOSED_STATUS, _('disposed')),
        (DESIRED_STATUS, _('desired')),
    )
    number = models.CharField(
        max_length=255,
        # translation
        verbose_name=_('article number'),
    )
    description = models.TextField(
        blank=True,
        null=True,
        # translation
        help_text=_('supports markdown'),
        verbose_name=_('description'),
    )
    manufacturer = models.ForeignKey(
        on_delete=models.PROTECT,
        related_name='manufactured_articles',
        to='inventory.Company',
        # translation
        verbose_name=_('manufacturer'),
    )
    vendor = models.ForeignKey(
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='marketed_articles',
        to='inventory.Company',
        # translation
        verbose_name=_('vendor'),
    )
    purchased = models.DateField(
        blank=True,
        null=True,
        # translation
        verbose_name=_('purchase date'),
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=BOUGHT_STATUS,
        # translation
        verbose_name=_('article status'),
    )
    price = models.DecimalField(
        blank=True,
        decimal_places=2,
        max_digits=9,
        null=True,
        # translation
        verbose_name=_('price'),
    )

    objects = ArticleManager()

    class Meta:
        ordering = ('number',)
        unique_together = ('manufacturer', 'number')
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __str__(self):
        return "{manufacturer} {number}".format(
            manufacturer=self.manufacturer,
            number=self.number,
        )


class AssemblyManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'assembly',
            'assembly__type',
            'configuration',
            'configuration__article',
            'configuration__article__manufacturer',
            'configuration__picture',
            'configuration__vehicle',
            'configuration__vehicle__vehicle',
            'configuration__vehicle__vehicle__klass',
            'configuration__vehicle__vehicle__klass__operator',
            'picture',
        )


class Assembly(models.Model):
    assembly = models.ForeignKey(
        on_delete=models.PROTECT,
        related_name='inventory_assemblies',
        to='rollingstock.Assembly',
        # translation
        verbose_name=_('assembly'),
    )
    configuration = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='assemblies',
        to='inventory.Configuration',
        # translation
        verbose_name=_('configuration')
    )
    picture = models.ForeignKey(
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='inventory_assemblies',
        to='gallery.Picture',
        # translation
        verbose_name=_('picture'),
    )

    objects = AssemblyManager()

    class Meta:
        ordering = ('assembly',)
        verbose_name = _('assembly')
        verbose_name_plural = _('assemblies')

    def __str__(self):
        return "{configuration}: {assembly}".format(configuration=self.configuration, assembly=self.assembly)


class Company(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        # translation
        verbose_name=_('company name'),
    )
    website = models.URLField(
        blank=True,
        null=True,
        # translation
        verbose_name=_('website'),
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('company')
        verbose_name_plural = _('companies')

    def __str__(self):
        return "{name}".format(name=self.name)


class ConfigurationManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'article',
            'article__manufacturer',
            'picture',
            'picture__author',
            'picture__license',
            'vehicle',
            'vehicle__vehicle',
            'vehicle__vehicle__klass',
            'vehicle__vehicle__klass__operator',
        ).prefetch_related(
            'assemblies',
        )


class Configuration(models.Model):

    UNCATEGORIZED = 0
    ENGINE_CATEGORY = 1
    SHUNTING_ENGINE_CATEGORY = 2
    SERVICE_ENGINE_CATEGORY = 3
    MOTOR_COACH_CATEGORY = 4
    FREIGHT_WAGON_CATEGORY = 5
    COACH_CATEGORY = 6

    CATEGORY_CHOICES = (
        (UNCATEGORIZED, _('uncategorized')),
        (ENGINE_CATEGORY, _('engine')),
        (SHUNTING_ENGINE_CATEGORY, _('shunting engine')),
        (SERVICE_ENGINE_CATEGORY, _('service engine')),
        (MOTOR_COACH_CATEGORY, _('motor coach')),
        (FREIGHT_WAGON_CATEGORY, _('freight wagon')),
        (COACH_CATEGORY, _('coach')),
    )

    article = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='configurations',
        to='inventory.Article',
        # translation
        verbose_name=_('article'),
    )
    picture = models.ForeignKey(
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='configurations',
        to='gallery.Picture',
        # translation
        verbose_name=_('picture'),
    )
    vehicle = models.OneToOneField(
        on_delete=models.PROTECT,
        related_name='configurations',
        to='inventory.Vehicle',
        # translation
        verbose_name=_('vehicle'),
    )
    description = models.TextField(
        blank=True,
        null=True,
        # translation
        help_text=_('supports markdown'),
        verbose_name=_('description'),
    )
    category = models.IntegerField(
        choices=CATEGORY_CHOICES,
        default=UNCATEGORIZED,
        verbose_name=_('category'),
    )

    objects = ConfigurationManager()
    tags = TaggableManager(
        blank=True,
    )

    class Meta:
        ordering = ('vehicle',)
        verbose_name = _('configuration')
        verbose_name_plural = _('configurations')

    def __str__(self):
        return "{article}: {vehicle}".format(article=self.article, vehicle=self.vehicle)


class VehicleManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'vehicle',
            'vehicle__klass',
            'vehicle__klass__operator',
            'picture',
        )


class Vehicle(models.Model):
    vehicle = models.ForeignKey(
        on_delete=models.PROTECT,
        related_name='invetory_vehicles',
        to='rollingstock.Vehicle',
        # translation
        verbose_name=_('vehicle'),
    )
    picture = models.ForeignKey(
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='inventory_vehicles',
        to='gallery.Picture',
        # translation
        verbose_name=_('picture'),
    )

    objects = VehicleManager()

    class Meta:
        ordering = ('vehicle',)
        verbose_name = _('vehicle')
        verbose_name_plural = _('vehicles')

    def __str__(self):
        return "{vehicle}".format(vehicle=self.vehicle)

    @property
    def html(self):
        return format_html("{}", self.vehicle.html)
