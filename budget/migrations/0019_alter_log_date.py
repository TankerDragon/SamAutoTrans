# Generated by Django 4.0.4 on 2022-08-15 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0018_alter_log_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
