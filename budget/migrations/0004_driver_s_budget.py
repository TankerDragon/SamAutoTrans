# Generated by Django 4.0.1 on 2022-06-30 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_alter_log_budget_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='s_budget',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=9, null=True),
        ),
    ]
