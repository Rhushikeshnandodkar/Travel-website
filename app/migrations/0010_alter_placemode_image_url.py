# Generated by Django 5.1.1 on 2024-10-14 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_placemode_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placemode',
            name='Image_url',
            field=models.URLField(blank=True, max_length=3000, null=True),
        ),
    ]