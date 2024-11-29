# Generated by Django 5.1.3 on 2024-11-29 21:36

import properties.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_amenity_remove_accommodation_amenities_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accommodation',
            name='amenities',
        ),
        migrations.DeleteModel(
            name='Amenity',
        ),
        migrations.AddField(
            model_name='accommodation',
            name='amenities',
            field=models.JSONField(blank=True, null=True, validators=[properties.models.validate_amenities]),
        ),
    ]
