# Generated by Django 4.0.4 on 2022-08-06 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0009_log_current_rate_log_original_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='gross',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True),
        ),
    ]
