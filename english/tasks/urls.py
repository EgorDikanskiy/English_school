from django.urls import path
from tasks import views

app_name = "tasks"

urlpatterns = [
    path("add_task/<int:pk>", views.AddTaskView.as_view(), name="add_task"),
    path("choose_student", views.ChooseStudentsView.as_view(), name="choose_student"),
]
