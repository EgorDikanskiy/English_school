from django.db import models
from teach.models import Kit


class TaskList(models.Model):
    kits = models.ManyToManyField(
        Kit,
        verbose_name='наборы',
        help_text='Выберите или добавьте набор',
    )

    user = models.ForeignKey(
        "users.Student",
        verbose_name="ученик",
        on_delete=models.SET_NULL,
        null=True,
        unique=True,
    )

    def __str__(self):
        return self.user.username
