# Generated by Django 3.2.4 on 2021-06-14 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_alter_child_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='activity',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='child',
            name='go_alone',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='child',
            name='image_rights',
            field=models.BooleanField(default=True),
        ),
    ]
