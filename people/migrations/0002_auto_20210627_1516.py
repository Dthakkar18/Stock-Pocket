# Generated by Django 3.2.4 on 2021-06-27 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='avg_share_price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='stock',
            name='shares',
            field=models.FloatField(),
        ),
    ]
