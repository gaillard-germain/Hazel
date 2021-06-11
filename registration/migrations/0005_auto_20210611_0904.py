# Generated by Django 3.2.4 on 2021-06-11 07:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_alter_child_birth_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('cell_phone', models.CharField(max_length=10, null=True)),
                ('family_situation', models.CharField(max_length=50, null=True)),
                ('relationship', models.CharField(max_length=50, null=True)),
                ('occupation', models.CharField(max_length=50, null=True)),
                ('job_address', models.CharField(max_length=200, null=True)),
                ('job_phone', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='AuthorizedPerson',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='address',
        ),
        migrations.RemoveField(
            model_name='legalguardian',
            name='address',
        ),
        migrations.RemoveField(
            model_name='legalguardian',
            name='job_address',
        ),
        migrations.AlterField(
            model_name='family',
            name='address',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.AddField(
            model_name='child',
            name='authorized_person',
            field=models.ManyToManyField(blank=True, related_name='authorized_person', to='registration.Adult'),
        ),
        migrations.AlterField(
            model_name='child',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='doctor', to='registration.adult'),
        ),
        migrations.AlterField(
            model_name='child',
            name='legal_guardian_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='legal_guardian_1', to='registration.adult'),
        ),
        migrations.AlterField(
            model_name='child',
            name='legal_guardian_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='legal_guardian_2', to='registration.adult'),
        ),
        migrations.DeleteModel(
            name='Doctor',
        ),
        migrations.DeleteModel(
            name='LegalGuardian',
        ),
    ]
