from django.conf import settings
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.views import generic

from users.forms import (
    CustomUserCreateForm,
    EditProfile,
    FormEmailPass,
    FormResetPassword,
)
from users.models import User
from users.utils import email_confirmation_token

__all__ = []

PATH = "users/"


class ProfileView(generic.View):
    template = PATH + "profile.html"
    context = {}

    def get(self, request, *args, **kwargs):
        self.context["model"] = request.user
        self.context["form"] = EditProfile(instance=request.user)

        return render(request, self.template, self.context)


class ChangeProfile(ProfileView):
    template = PATH + "profile_change.html"
    succses_url = "/auth/profile/"
    context = {}
    form_class = EditProfile

    def post(self, request, *args, **kwargs):
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            file = request.FILES.get("avatar")
            if file:
                request.user.avatar = file
                request.user.save()
        self.context["form"] = form
        return render(request, self.template, self.context)


class RegisterView(generic.FormView):
    template_name = PATH + "auth/register.html"
    form_class = CustomUserCreateForm
    success_url = '/auth/profile/'

    def form_valid(self, form):
        normalize_email = User.objects.normalize_email(
            form.cleaned_data["email"],
        )
        form.is_active = settings.DEFAULT_USER_IS_ACTIVE
        form.email = normalize_email

        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)


class ActivateView(generic.View):
    context = {}

    def get(self, request, **kwargs):
        try:
            user = User.objects.get(**kwargs)
        except User.DoesNotExist:
            user = None
        if isinstance(user, User) and not user.is_active:
            user.is_active = True
            user.token = email_confirmation_token.make_token(user)
            user.token_active = False
            user.save()
            login(
                request,
                user,
                "OnTheHook.backends.ModifyLogin",
            )
            return redirect(reverse("users:profile"))

        return HttpResponseNotAllowed("Ошибка")


class ResetPassword(generic.View):
    tempalte_name = PATH + "auth/password_reset.html"
    context = {}
    form_class = FormEmailPass

    def get(self, request, **kwargs):
        self.context["form"] = self.form_class(None)
        return render(request, self.tempalte_name, self.context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if not form.is_valid():
            self.context["form"] = form
            return render(request, self.tempalte_name, self.context)
        email = form.cleaned_data.get("email")
        try:
            user = User.objects.by_mail(email)
        except User.DoesNotExist:
            user = False

        if user:
            user.token = email_confirmation_token.make_token(user)
            user.token_active = True
            user.save()

            link = f"http://{get_current_site(request)}" + reverse(
                "users:change_password",
                args=[user.pk, user.token],
            )

            html_message = render_to_string(
                "change_email.html",
                {
                    "link": link,
                    "username": user.username,
                },
            )

            plain_message = strip_tags(html_message)

            msg = EmailMultiAlternatives(
                "Сброс пароля",
                plain_message,
                None,
                [email],
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send()

        return redirect(reverse("users:reset_password_done"))


class ChangePassword(generic.FormView):
    template_name = PATH + "auth/password_change.html"
    context = {}
    form_class = FormResetPassword
    success_url = "/auth/profile/"
    user = ...

    def get(self, request, **kwargs):
        try:
            self.user = User.objects.get(**self.kwargs)
        except User.DoesNotExist:
            self.user = False

        if self.user:
            return super().get(request, **kwargs)
        return redirect(reverse("catalog:spot_list"))

    def form_valid(self, form) -> HttpResponse:
        user = self.user
        user.set_password(form.cleaned_data.get("password1"))
        user.token_active = False
        user.save()
        login(self.request, user, "OnTheHook.backend.ModifyLogin")

        return super().form_valid(form)


class ChangePasswordDone(generic.TemplateView):
    template_name = PATH + "auth/password_change_done.html"


class ResetPasswordDone(generic.TemplateView):
    template_name = PATH + "auth/password_reset_done.html"
