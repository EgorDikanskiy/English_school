from django.contrib.auth.models import UserManager

__all__ = []


class CustomUserManager(UserManager):
    def create_superuser(
        self,
        username,
        email,
        password,
        **extra_fields,
    ):
        superuser = super().create_user(
            username,
            email,
            password,
            **extra_fields,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()

    def by_mail(
        self,
        mail,
    ):
        return super().get_queryset().get(email=mail)
