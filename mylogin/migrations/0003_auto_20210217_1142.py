# Generated by Django 3.1.5 on 2021-02-17 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylogin', '0002_auto_20210216_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='bio',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]