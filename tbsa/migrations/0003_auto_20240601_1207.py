# Generated by Django 3.2.25 on 2024-06-01 09:07

from django.db import migrations, models
import tbsa.models


class Migration(migrations.Migration):

    dependencies = [
        ('tbsa', '0002_alter_tbsa_is_inhalation'),
    ]

    operations = [
        migrations.AddField(
            model_name='tbsa',
            name='first_dose_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tbsa',
            name='second_dose_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tbsa',
            name='third_dose_amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='tbsa_image',
            name='image',
            field=models.ImageField(upload_to=tbsa.models.upload_to),
        ),
        migrations.AlterField(
            model_name='tbsa_image',
            name='image_type',
            field=models.CharField(choices=[('H', 'Hand'), ('B', 'Burn')], max_length=10),
        ),
    ]