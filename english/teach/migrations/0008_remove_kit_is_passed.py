# Generated by Django 5.0.7 on 2024-08-17 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teach', '0007_kit_is_passed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kit',
            name='is_passed',
        ),
    ]
