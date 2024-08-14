from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core import validators
from django.db import models

from users.managers import CustomUserManager

__all__ = []


class User(AbstractBaseUser, PermissionsMixin):
    def path_to_save(self, file_name):
        return f"avatars/{self.pk}_{file_name}"

    username = models.CharField(
        verbose_name="Пользовательское имя",
        help_text=(
            "имя отображаемое для всех пользователей (nickname)."
            "\nДопустимые символы: латиница, цифры, @|.|+|-|_"
        ),
        unique=True,
        max_length=25,
        validators=[
            validators.MaxLengthValidator(25),
            validators.MinLengthValidator(4),
            UnicodeUsernameValidator(),
        ],
    )

    email = models.EmailField(
        verbose_name="Почта",
        help_text="почтовый адрес",
        unique=True,
    )

    first_name = models.CharField(
        verbose_name="Имя",
        blank=True,
        null=True,
        max_length=150,
        default="отсутствует",
    )

    last_name = models.CharField(
        verbose_name="Фамилия",
        blank=True,
        null=True,
        max_length=150,
        default="отсутствует",
    )

    date_joined = models.DateTimeField(
        verbose_name="Дата присоединения",
        help_text="день и время, когда пользователь зарегистрировался",
        auto_now_add=True,
        null=True,
        blank=True,
    )

    avatar = models.ImageField(
        verbose_name="Аватарка",
        upload_to=path_to_save,
        default="/avatars/base.jpg",
    )

    birthday = models.DateField(
        verbose_name="День рождения",
        help_text="ДД.ММ.ГГГГ",
        blank=True,
        null=True,
    )

    is_superuser = models.BooleanField(
        verbose_name="владыка",
        help_text="тебе дозволенно всё",
        default=False,
    )

    is_staff = models.BooleanField(
        verbose_name="персонал",
        help_text="",
        default=False,
    )
    is_moderator = models.BooleanField(
        verbose_name="модератор",
        help_text="",
        default=False,
    )

    is_redactor = models.BooleanField(
        verbose_name="редактор",
        help_text="",
        default=False,
    )

    is_teacher = models.BooleanField(
        verbose_name="учитель",
        default=False,
    )

    is_student = models.BooleanField(
        verbose_name="ученик",
        default=False,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    @property
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return "/media/avatars/base.jpg"

    def __str__(self):
        return self.username
