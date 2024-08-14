# Generated by Django 5.0.7 on 2024-07-26 12:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(help_text='Введите слово', max_length=150, unique=True, validators=[django.core.validators.MaxLengthValidator(150)], verbose_name='слово')),
                ('translation', models.CharField(help_text='Введите перевод слова', max_length=150, unique=True, validators=[django.core.validators.MaxLengthValidator(150)], verbose_name='перевод')),
            ],
        ),
    ]
