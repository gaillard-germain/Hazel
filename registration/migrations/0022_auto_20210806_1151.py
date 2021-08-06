# Generated by Django 3.2.4 on 2021-08-06 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0021_family_quotient'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nom')),
                ('age_min', models.IntegerField()),
                ('age_max', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Catégorie',
            },
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('name',), name='category_unique'),
        ),
        migrations.AlterField(
            model_name='child',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='registration.category', verbose_name='Catégorie'),
        ),
    ]