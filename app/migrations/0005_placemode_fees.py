# Generated by Django 4.2.16 on 2024-10-02 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_placemode_best_time_to_visit_placemode_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='placemode',
            name='Fees',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]