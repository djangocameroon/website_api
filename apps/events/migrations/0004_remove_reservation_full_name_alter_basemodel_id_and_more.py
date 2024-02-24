# Generated by Django 5.0.1 on 2024-02-24 19:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_basemodel_id_alter_eventtag_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='full_name',
        ),
        migrations.AlterField(
            model_name='basemodel',
            name='id',
            field=models.UUIDField(default='d12194e7-b8c7-4acd-83c0-3e8fef6a8bb9', editable=False, help_text='Unique identifier for this object.', primary_key=True, serialize=False, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='event',
            name='speaker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.speaker'),
        ),
        migrations.AlterField(
            model_name='eventtag',
            name='id',
            field=models.UUIDField(default='9ffec15e-b6d5-4735-b3c7-d31d05125e7a', editable=False, help_text='Unique identifier for this object.', primary_key=True, serialize=False, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='id',
            field=models.UUIDField(default='e9ead250-1784-4cc1-995b-84274b230d56', editable=False, help_text='Unique identifier for this object.', primary_key=True, serialize=False, verbose_name='id'),
        ),
        migrations.AlterField(
            model_name='speaker',
            name='last_updated_by',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
