from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Prefetch
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.views import generic
from tasks.models import TaskList

from users.forms import (
    CustomTeacherCreateForm,
    CustomStudentCreateForm,
    EditProfile,
    FormEmailPass,
    FormResetPassword,
    CustomLoginForm,
    ChoiceStatusForm,
    # AddStudentForm,
)
from users.models import User, Teacher, Student
from users.utils import email_confirmation_token

__all__ = []

PATH = "users/"


class ProfileView(generic.View):
    template = PATH + "profile.html"
    context = {}

    def get(self, request, *args, **kwargs):
        if self.request.user.is_student:
            user_id = self.request.user.id
            tasks = TaskList.objects.get(user_id=user_id)
            self.context['tasks'] = tasks.kits.all()
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
        return redirect(self.succses_url)


class RegisterStudentView(generic.View):
    template_name = PATH + "auth/register.html"
    success_url = '/auth/profile/'
    context = {}

    def get(self, request):
        form = CustomStudentCreateForm(request.POST)
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = CustomStudentCreateForm(request.POST)
        if form.is_valid():
            normalize_email = User.objects.normalize_email(
                form.cleaned_data["email"],
            )
            form.is_active = settings.DEFAULT_USER_IS_ACTIVE
            form.email = normalize_email
            user = form.save(commit=False)
            user.save()
        return redirect(self.success_url)


class RegisterTeacherView(generic.View):
    template_name = PATH + "auth/register.html"
    success_url = '/auth/profile/'
    context = {}

    def get(self, request):
        form = CustomTeacherCreateForm(request.POST)
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request):
        form = CustomTeacherCreateForm(request.POST)
        if form.is_valid():
            normalize_email = User.objects.normalize_email(
                form.cleaned_data["email"],
            )
            form.is_active = settings.DEFAULT_USER_IS_ACTIVE
            form.email = normalize_email
            user = form.save(commit=False)
            user.save()
        return redirect(self.success_url)


class RegisterView(generic.View):
    template = PATH + "auth/choice_status.html"
    context = {}

    def get(self, request):
        form = ChoiceStatusForm(request.POST)
        self.context['form'] = form
        return render(request, self.template, self.context)

    def post(self, request):
        form = ChoiceStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data['status']
        if status == '1':
            return redirect('student/')
        return redirect('teacher/')


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


class LoginView(generic.View):
    template = PATH + "auth/login.html"
    context = {}

    def get(self, request):
        form = CustomLoginForm(request.POST)
        self.context['form'] = form
        return render(request, self.template, self.context)

    def post(self, request):
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('/auth/profile/')
        message = 'Введите верный логин и пароль!'
        return render(request, self.template, context={'form': form, 'message': message})


# class AddStudentView(generic.View):
#     template = PATH + "auth/add_student.html"
#     context = {}
#     success_url = 'profile/'
#
#     def get(self, request):
#         user_id = self.request.user.id
#         user = Teacher.objects.get(pk=user_id)
#         form = AddStudentForm(instance=user)
#         self.context['form'] = form
#         return render(request, self.template, self.context)
#
#     def post(self, request):
#         user_id = self.request.user.id
#         user = Teacher.objects.get(pk=user_id)
#         form = AddStudentForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect(self.success_url)
