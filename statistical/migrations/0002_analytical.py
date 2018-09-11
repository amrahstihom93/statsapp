# Generated by Django 2.1 on 2018-08-30 08:44

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('statistical', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='analytical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analytical_id', models.CharField(blank=True, max_length=250)),
                ('analytical_name', models.CharField(blank=True, max_length=250)),
                ('analytical_method', models.CharField(blank=True, max_length=250)),
                ('analytical_calculated_value', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('parameters', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('test', models.CharField(blank=True, max_length=250)),
                ('dataset_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='upload.Dataset')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]