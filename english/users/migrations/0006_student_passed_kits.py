# Generated by Django 5.0.7 on 2024-08-17 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teach', '0008_remove_kit_is_passed'),
        ('users', '0005_alter_teacher_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='passed_kits',
            field=models.ManyToManyField(to='teach.kit', verbose_name='пройденные наборы'),
        ),
    ]
