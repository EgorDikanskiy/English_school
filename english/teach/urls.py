from django.urls import path, include
from rest_framework import routers
from teach import views, api

router = routers.DefaultRouter()
router.register("objects", api.ObjectsViewSet)

app_name = "teach"

urlpatterns = [
    path("", views.StartView.as_view(), name="teach"),
    path("kit/<int:kit_pk>/card/<int:card_pk>/correctly/", views.CorrectlyView.as_view(), name="correctly"),
    path("kit/<int:kit_pk>/card/<int:card_pk>/wrong/", views.WrongView.as_view(), name="wrong"),
    path("kits/", views.KitsView.as_view(), name="kits"),
    path("kit/<int:pk>", views.KitDetailView.as_view(), name="kit_detail"),
    path("kit_example/<int:pk>", views.KitDetailExampleView.as_view(), name="kit_detail_example"),
    path(
        "kit/<int:kit_pk>/card/<int:card_pk>/",
        views.KitCardDetailView.as_view(),
        name="kit_card",
    ),
    path(
        "kit/<int:kit_pk>/card_example/<int:card_pk>/",
        views.KitCardExampleView.as_view(),
        name="kit_card_example",
    ),
    path(
        "kit_create",
        views.KitCreateView.as_view(),
        name="kit_create",
    ),
    path(
        "card_create",
        views.CardCreateView.as_view(),
        name="card_create",
    ),
    path(
        'warning_stuf',
        views.WarningStufView.as_view(),
        name="warning_stuf",
    ),
    path(
        'my_kits',
        views.MyKitsView.as_view(),
        name="my_kits",
    ),
    path(
        'about',
        views.AboutView.as_view(),
        name="about",
    ),
    path(
        'passed_kit',
        views.PassedKitView.as_view(),
        name="passed_kit",
    ),
    path(
        'kit_edit/<int:pk>',
        views.KitEditView.as_view(),
        name="kit_edit",
    ),
    path(
        'warning_user',
        views.WarningUserView.as_view(),
        name="warning_user",
    ),
    path(
        "api/",
        include(router.urls),
    ),
    path(
        "api-auth/",
        include(
            "rest_framework.urls",
            namespace="rest_framework",
        ),
    ),
    path("add_student/<int:pk>", views.AddStudentView.as_view(), name="add_student"),
]
