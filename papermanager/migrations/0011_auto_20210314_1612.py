# Generated by Django 3.1.5 on 2021-03-14 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('papermanager', '0010_auto_20210303_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='labels',
            field=models.ManyToManyField(blank=True, to='papermanager.Label'),
        ),
    ]
