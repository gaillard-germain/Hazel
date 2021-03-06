# Generated by Django 3.2.4 on 2021-07-20 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20210719_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='booking.slot', verbose_name='Créneau'),
        ),
        migrations.AlterField(
            model_name='period',
            name='end_date',
            field=models.DateField(verbose_name='Date fin'),
        ),
        migrations.AlterField(
            model_name='period',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Nom'),
        ),
        migrations.AlterField(
            model_name='period',
            name='start_date',
            field=models.DateField(verbose_name='Date début'),
        ),
    ]
