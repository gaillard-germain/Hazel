# Generated by Django 3.2.4 on 2021-08-06 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20210806_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='slot',
        ),
        migrations.DeleteModel(
            name='Agenda',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
    ]
