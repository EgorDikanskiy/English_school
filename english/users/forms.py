from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import CharField, EmailField, Form, ModelForm, PasswordInput

from users.models import User

__all__ = [
    "CustomUserCreateForm",
    "CustomUserChangeForm",
]


class CustomUserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "custom_input"

    password1 = CharField(label="Введите пароль", widget=PasswordInput())
    password2 = CharField(label="Подтвердите пароль", widget=PasswordInput())

    class Meta:
        model = User
        fields = (
            User.username.field.name,
            User.email.field.name,
            "password1",
            "password2",
        )


class CustomLoginForm(Form):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "custom_input"

    username = CharField(label="Введите имя пользователя")
    password = CharField(label="Введите пароль", widget=PasswordInput())


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
        exclude = (
            User.avatar.field.name,
            User.password.field.name,
        )


class EditProfile(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "custom_input"
        self.fields["avatar"].required = False
        self.fields['is_teacher'].widget.attrs.update({'class': ''})
        self.fields['is_student'].widget.attrs.update({'class': ''})

    class Meta:
        model = User
        fields = (
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
            User.avatar.field.name,
            User.is_teacher.field.name,
            User.is_student.field.name,
        )


class FormEmailPass(Form):
    email = EmailField(
        required=True,
        label="Почта",
    )


class FormResetPassword(Form):
    password1 = CharField(label="Введите пароль", widget=PasswordInput())
    password2 = CharField(label="Подтвердите пароль", widget=PasswordInput())
