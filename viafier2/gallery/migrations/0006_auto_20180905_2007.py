# Generated by Django 2.1.1 on 2018-09-05 20:07

from django.db import migrations, models
import gallery.models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_auto_20180905_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vector',
            name='vector',
            field=models.FileField(upload_to='gallery/vectors/', validators=[gallery.models.validate_svg], verbose_name='vector'),
        ),
    ]
