# Generated by Django 3.2.4 on 2021-06-03 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=10, null=True)),
                ('road', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zip_code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AuthorizedPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('cell_phone', models.CharField(blank=True, max_length=10, null=True)),
                ('relationship', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LegalGuardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('family_situation', models.CharField(blank=True, max_length=50, null=True)),
                ('occupation', models.CharField(blank=True, max_length=50, null=True)),
                ('job_phone', models.CharField(blank=True, max_length=10, null=True)),
                ('cell_phone', models.CharField(blank=True, max_length=10, null=True)),
                ('email', models.EmailField(blank=True, max_length=50, null=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.address')),
                ('job_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_address', to='registration.address')),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lastname', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.address')),
            ],
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('birth_date', models.DateTimeField()),
                ('grade', models.CharField(blank=True, max_length=10, null=True)),
                ('school', models.CharField(blank=True, max_length=50, null=True)),
                ('info', models.TextField(blank=True, null=True)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='registration.doctor')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.family')),
                ('legal_guardian_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='legal_guardian_1', to='registration.legalguardian')),
                ('legal_guardian_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='legal_guardian_2', to='registration.legalguardian')),
            ],
        ),
    ]
