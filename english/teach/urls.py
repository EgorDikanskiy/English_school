from django.urls import path

from teach import views

app_name = "teach"

urlpatterns = [
    path("", views.StartView.as_view(), name="teach"),
    path("kit/<int:kit_pk>/card/<int:card_pk>/correctly/", views.CorrectlyView.as_view(), name="correctly"),
    path("kit/<int:kit_pk>/card/<int:card_pk>/wrong/", views.WrongView.as_view(), name="wrong"),
    path("kits/", views.KitsView.as_view(), name="kits"),
    path("kit/<int:pk>", views.KitDetailView.as_view(), name="kit_detail"),
    path(
        "kit/<int:kit_pk>/card/<int:card_pk>/",
        views.KitCardDetailView.as_view(),
        name="kit_card",
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
    )
]
