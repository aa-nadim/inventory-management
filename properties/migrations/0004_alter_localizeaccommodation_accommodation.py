# Generated by Django 5.1.3 on 2024-12-04 10:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0003_partition_localize_accommodation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localizeaccommodation',
            name='accommodation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.accommodation'),
        ),
    ]