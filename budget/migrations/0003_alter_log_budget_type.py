# Generated by Django 4.0.1 on 2022-06-30 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_alter_log_bol_number_alter_log_pcs_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='budget_type',
            field=models.CharField(choices=[('D', 'driver'), ('L', 'lane'), ('R', 'recovery'), ('S', 'dirilis')], max_length=1),
        ),
    ]
