# Generated by Django 2.0.8 on 2018-08-18 19:00

from django.db import migrations
import taggit_selectize.managers


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_configuration_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='tags',
            field=taggit_selectize.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
