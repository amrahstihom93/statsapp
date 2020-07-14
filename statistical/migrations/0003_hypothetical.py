# Generated by Django 2.1 on 2020-07-03 08:20

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('statistical', '0002_analytical'),
    ]

    operations = [
        migrations.CreateModel(
            name='hypothetical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hypothetical_id', models.CharField(blank=True, max_length=250)),
                ('hypothetical_name', models.CharField(blank=True, max_length=250)),
                ('hypothetical_method', models.CharField(blank=True, max_length=250)),
                ('hypothetical_calculated_value', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('parameters', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('test', models.CharField(blank=True, max_length=250)),
                ('dataset_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='upload.Dataset')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
