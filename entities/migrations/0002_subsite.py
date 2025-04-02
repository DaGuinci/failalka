# Generated by Django 5.1.6 on 2025-04-02 19:53

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subsite',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('location', models.JSONField(blank=True, null=True)),
                ('chrono', models.JSONField(blank=True, null=True)),
                ('justification', models.TextField(blank=True, null=True)),
                ('settle_type', models.CharField(blank=True, max_length=150, null=True)),
                ('material', models.CharField(blank=True, max_length=150, null=True)),
                ('remains', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.site')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
