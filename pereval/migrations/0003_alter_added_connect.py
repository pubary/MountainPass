# Generated by Django 4.1.5 on 2023-03-18 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0002_alter_coords_latitude_alter_coords_longitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='added',
            name='connect',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]