# Generated by Django 3.2.25 on 2024-05-28 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FirstAidsProcedure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procedure', models.CharField(max_length=100)),
                ('procedure_for_degree', models.CharField(max_length=100)),
                ('procedure_order', models.IntegerField()),
            ],
        ),
    ]
