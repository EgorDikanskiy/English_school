# Generated by Django 5.0.7 on 2024-08-15 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_student_user_is_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='all_answers_count',
            field=models.IntegerField(default=0, verbose_name='кол-во ответов'),
        ),
        migrations.AddField(
            model_name='user',
            name='correct_answers_count',
            field=models.IntegerField(default=0, verbose_name='кол-во правильных ответов ответов'),
        ),
    ]
