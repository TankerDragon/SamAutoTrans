# Generated by Django 4.0.3 on 2022-05-20 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0011_rename_dr_type_driver_driver_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, null=True)),
                ('last_name', models.CharField(max_length=20, null=True)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('user_type', models.CharField(choices=[('D', 'dispatcher'), ('U', 'updater')], default='U', max_length=1)),
                ('is_active', models.BooleanField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Staff_driver_group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.driver')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.staff')),
            ],
        ),
    ]
