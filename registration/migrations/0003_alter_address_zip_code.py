# Generated by Django 3.2.4 on 2021-06-08 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_address_authorizedperson_child_doctor_family_legalguardian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(max_length=5),
        ),
    ]
