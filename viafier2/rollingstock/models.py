from collections import defaultdict
from django.db import models
from django.utils.html import format_html
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
        return "{name} ({abbrev})".format(name=self.name, abbrev=self.abbrev)


class VehicleKlass(models.Model):
    klass = models.CharField(
        max_length=255,
        unique=True,
        # translation
        verbose_name=_('class'),
    )
    revision = models.CharField(
        blank=True,
        max_length=255,
        null=True,
        # translation
        verbose_name=_('revision'),
    )
    revision_hidden = models.BooleanField(
        default=False,
        # translation
        help_text=_('for classes that have a revision that is not displayed on the vehicle'),
        verbose_name=_('hide revision'),
    )
    operator = models.ForeignKey(
        on_delete=models.PROTECT,
        related_name='vehicle_klasses',
        to='rollingstock.Operator',
        # translation
        verbose_name=_('operator'),
    )
    description = models.TextField(
        blank=True,
        # translation
        help_text=_('supports markdown'),
        verbose_name=_('description'),
    )

    class Meta:
        ordering = ('operator', 'klass',)
        verbose_name = _('vehicle class')
        verbose_name_plural = _('vehicle classes')

    def __str__(self):
        str_repr = "{} {}".format(self.operator.abbrev, self.klass)
        if self.revision and not self.revision_hidden:
            str_repr = "{} {}".format(str_repr, self.revision)
        return str_repr

    @property
    def html(self):
        str_repr = format_html("{} {}", self.operator.abbrev, self.klass)
        if self.revision and not self.revision_hidden:
            str_repr = format_html("{}<sup>{}</sup>", str_repr, self.revision)
        return str_repr


class VehicleManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'klass',
            'klass__operator',
            'picture',
        )


class Vehicle(models.Model):
    klass = models.ForeignKey(
        on_delete=models.PROTECT,
        to='rollingstock.VehicleKlass',
        related_name='vehicles',
        # translation
        verbose_name=_('vehicle class')
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

    objects = VehicleManager()

    class Meta:
        ordering = ('klass', 'number')
        verbose_name = _('vehicle')
        verbose_name_plural = _('vehicles')

    def __str__(self):
        str_repr = "{}".format(self.klass)
        if self.number:
            str_repr = "{} {}".format(str_repr, self.number)
        return str_repr

    @property
    def html(self):
        str_repr = self.klass.html
        if self.number:
            str_repr = format_html("{} {}", str_repr, self.number)
        return str_repr

