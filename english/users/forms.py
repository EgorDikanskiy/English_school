from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import CharField, EmailField, Form, ModelForm, PasswordInput, ChoiceField, ModelMultipleChoiceField

from users.models import Teacher, Student, User


# class AddStudentForm(ModelForm):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#         for field in self.visible_fields():
#             field.field.widget.attrs["class"] = "custom_input"
#         self.fields['students'].widget.attrs.update({'class': 'custom_input cards_input'})
#
#     class Meta:
#         model = Teacher
#         fields = (
#             Teacher.students.field.name,
#         )


class ChoiceStatusForm(Form):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "custom_input"

    CHOICES = (
        ("1", "Ученик"),
        ("2", "Учитель"),
    )

    status = ChoiceField(choices=CHOICES, label='Статус пользователя')


class CustomTeacherCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "custom_input"

    password1 = CharField(label="Введите пароль", widget=PasswordInput())
    password2 = CharField(label="Подтвердите пароль", widget=PasswordInput())

    class Meta:
        model = Teacher
        fields = (
            Teacher.username.field.name,
            Teacher.email.field.name,
            "password1",
            "password2",
        )


class CustomStudentCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "custom_input"

    password1 = CharField(label="Введите пароль", widget=PasswordInput())
    password2 = CharField(label="Подтвердите пароль", widget=PasswordInput())

    class Meta:
        model = Student
        fields = (
            Student.username.field.name,
            Student.email.field.name,
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

    class Meta:
        model = User
        fields = (
            User.first_name.field.name,
            User.last_name.field.name,
            User.email.field.name,
            User.avatar.field.name,
        )


class FormEmailPass(Form):
    email = EmailField(
        required=True,
        label="Почта",
    )


class FormResetPassword(Form):
    password1 = CharField(label="Введите пароль", widget=PasswordInput())
    password2 = CharField(label="Подтвердите пароль", widget=PasswordInput())
