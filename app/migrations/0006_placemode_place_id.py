# Generated by Django 4.2.16 on 2024-10-02 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_placemode_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='placemode',
            name='place_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]