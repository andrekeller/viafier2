from django.db import models
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
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
    price = models.DecimalField(
        blank=True,
        decimal_places=2,
        max_digits=9,
        null=True,
        # translation
        verbose_name=_('price'),
    )

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


class Assembly(models.Model):
    assembly = models.ForeignKey(
        on_delete=models.PROTECT,
        related_name='inventory_assemblies',
        to='rollingstock.Assembly',
        # translation
        verbose_name=_('assembly'),
    )
    configuration = models.ForeignKey(
        on_delete=models.PROTECT,
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


class Configuration(models.Model):
    article = models.ForeignKey(
        on_delete=models.PROTECT,
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

    class Meta:
        ordering = ('article',)
        verbose_name = _('configuration')
        verbose_name_plural = _('configurations')

    def __str__(self):
        return "{article}: {vehicle}".format(article=self.article, vehicle=self.vehicle)


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

    class Meta:
        ordering = ('vehicle',)
        verbose_name = _('vehicle')
        verbose_name_plural = _('vehicles')

    def __str__(self):
        return "{vehicle}".format(vehicle=self.vehicle)
