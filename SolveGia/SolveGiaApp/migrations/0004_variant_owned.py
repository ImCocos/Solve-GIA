# Generated by Django 4.2.1 on 2023-05-23 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SolveGiaApp', '0003_library'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='owned',
            field=models.BooleanField(default=False),
        ),
    ]
