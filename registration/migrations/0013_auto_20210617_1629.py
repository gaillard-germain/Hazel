# Generated by Django 3.2.4 on 2021-06-17 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0012_auto_20210617_1559'),
    ]

    operations = [
        migrations.RenameField(
            model_name='family',
            old_name='address',
            new_name='home_address',
        ),
        migrations.RenameField(
            model_name='family',
            old_name='phone',
            new_name='home_phone',
        ),
        migrations.RenameField(
            model_name='family',
            old_name='name',
            new_name='use_name',
        ),
    ]