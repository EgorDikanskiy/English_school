from django.contrib.auth import views as djangoviews
from django.contrib.auth.decorators import login_required
from django.urls import path

from users.utils import redirect_required
import users.views as views

app_name = "users"

urlpatterns = [
    path(
        "profile/",
        login_required(views.ProfileView.as_view()),
        name="profile",
    ),
    path(
        "profile/change/",
        login_required(views.ChangeProfile.as_view()),
        name="change_profile",
    ),
    path(
        "register/",
        views.RegisterView.as_view(),
        name="register",
    ),
    path(
        "activate/<int:pk>/<str:token>/",
        views.ActivateView.as_view(),
        name="activate",
    ),
    path(
        "login/",
        djangoviews.LoginView.as_view(
            template_name="users/auth/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        djangoviews.LogoutView.as_view(
            template_name="users/auth/logout.html",
        ),
        name="logout",
    ),
    path(
        "password_change/<int:pk>/<str:token>/",
        views.ChangePassword.as_view(),
        name="change_password",
    ),
    path(
        "password_change/done/",
        redirect_required(views.ChangePasswordDone.as_view()),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        views.ResetPassword.as_view(),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        redirect_required(views.ResetPasswordDone.as_view()),
        name="reset_password_done",
    ),
]
