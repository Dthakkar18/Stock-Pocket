# Generated by Django 3.2.4 on 2021-08-27 03:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_auto_20210826_2204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agent',
            old_name='organization_id',
            new_name='organization',
        ),
    ]
