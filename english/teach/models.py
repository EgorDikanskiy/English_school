from django.db import models
from django.core import validators


class Card(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="пользователь",
        on_delete=models.SET_NULL, null=True,
    )

    word = models.CharField(
        verbose_name="слово",
        max_length=150,
        validators=[validators.MaxLengthValidator(150)],
        help_text="Введите слово",
        unique=False,
    )

    translation = models.CharField(
        verbose_name="перевод",
        max_length=150,
        validators=[validators.MaxLengthValidator(150)],
        help_text="Введите перевод слова",
        unique=False,
    )

    def __str__(self):
        return self.word


class Kit(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name="пользователь",
        on_delete=models.SET_NULL, null=True,
    )

    name = models.CharField(
        verbose_name="название",
        max_length=150,
        validators=[validators.MaxLengthValidator(150)],
        help_text="Введите название",
        unique=True,
    )

    cards = models.ManyToManyField(
        Card,
        verbose_name='карточки',
        help_text='Выберите или добавьте карточку',
    )

    class Meta:
        verbose_name = "набор"
        verbose_name_plural = "наборы"

    def __str__(self):
        return self.name
