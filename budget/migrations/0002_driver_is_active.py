# Generated by Django 4.0.3 on 2022-04-20 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='is_active',
            field=models.BooleanField(default=1),
        ),
    ]
