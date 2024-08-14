from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponseRedirect
import six

__all__ = []


class EmailConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """
        user: models.User
        """
        return (
            six.text_type(user.pk)
            + user.email
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


def redirect_required(func):
    def wrapper(request, *args, **kwargs):
        if request.META.get("HTTP_REFERER"):
            return func(request, *args, **kwargs)

        return HttpResponseRedirect("/catalog/")

    return wrapper


email_confirmation_token = EmailConfirmationTokenGenerator()
