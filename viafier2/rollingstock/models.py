from collections import defaultdict
from django.db import models
from django.utils.translation import gettext_lazy as _


class Assembly(models.Model):
    name = models.CharField(
        max_length=255,
        # translation
        verbose_name=_('assembly name'),
    )
    number = models.CharField(
        blank=True,
        max_length=255,
        null=True,
        # translation
        verbose_name=_('assembly number'),
    )
    type = models.ForeignKey(
        on_delete=models.PROTECT,
        related_name='assemblies',
        to='rollingstock.AssemblyType',
        # translation
        verbose_name=_('assembly type')
    )
    picture = models.ForeignKey(
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='assemblies',
        to='gallery.Picture',
        # translation
        verbose_name=_('picture')
    )

    class Meta:
        ordering = ("name", "number", "type")
        verbose_name = _('Assembly')
        verbose_name_plural = _('Assemblies')

    def __str__(self):
        if self.number:
            return "{name} {number} ({type})".format(
                name=self.name,
                number=self.number,
                type=self.type,
            )
        else:
            return "{name} ({type})".format(
                name=self.name,
                type=self.type,
            )


class AssemblyType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        # translation
        verbose_name=_('assembly type name')
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('Assembly type')
        verbose_name_plural = _('Assembly types')

    def __str__(self):
        return "{name}".format(name=self.name)


class Operator(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        # translation
        verbose_name=_('operator name')
    )
    abbrev = models.CharField(
        max_length=255,
        unique=True,
        # translation
        verbose_name=_('abbreviated operator name')
    )

    class Meta:
        ordering = ('abbrev', 'name',)
        verbose_name = _('operator')
        verbose_name_plural = _('operators')

    def __str__(self):
        return "{name}".format(name=self.name)


class VehicleKlass(models.Model):
    klass = models.CharField(
        max_length=255,
        unique=True,
        # translation
        verbose_name=_('class'),
    )
    description = models.TextField(
        blank=True,
        # translation
        help_text=_('supports markdown'),
        verbose_name=_('description'),
    )

    class Meta:
        ordering = ('klass',)
        verbose_name = _('vehicle class')
        verbose_name_plural = _('vehicle classes')

    def __str__(self):
        return "{klass}".format(klass=self.klass)


class Vehicle(models.Model):
    klass = models.ForeignKey(
        on_delete=models.PROTECT,
        to='rollingstock.VehicleKlass',
        related_name='vehicles',
        # translation
        verbose_name=_('vehicle class')
    )
    operator = models.ForeignKey(
        on_delete=models.PROTECT,
        related_name='vehicles',
        to='rollingstock.Operator',
        # translation
        verbose_name=_('operator'),
    )
    number = models.CharField(
        blank=True,
        max_length=255,
        null=True,
        # translation
        verbose_name=_('vehicle number'),
    )
    description = models.TextField(
        blank=True,
        null=True,
        # translation
        help_text=_('supports markdown'),
        verbose_name=_('description'),
    )
    picture = models.ForeignKey(
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='vehicles',
        to='gallery.Picture',
        # translation
        verbose_name=_('picture'),
    )

    class Meta:
        ordering = ('operator', 'klass', 'number')
        verbose_name = _('vehicle')
        verbose_name_plural = _('vehicles')

    def __str__(self):
        if self.number:
            return "{operator} {klass} {number}".format(
                operator=self.operator,
                klass=self.klass,
                number=self.number,
            )
        else:
            return "{operator} {klass}".format(
                operator=self.operator,
                klass=self.klass,
            )
