# Generated by Django 2.1 on 2018-09-02 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_article_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.IntegerField(choices=[(0, 'bought'), (1, 'ordered'), (2, 'sold'), (3, 'disposed'), (3, 'desired')], default=0, verbose_name='article status'),
        ),
    ]
