# Generated by Django 5.1 on 2024-10-16 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
