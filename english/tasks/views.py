from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from tasks.forms import AddTaskForm, ChooseStudentForm
from tasks.models import TaskList


class ChooseStudentsView(View):
    template_name = "tasks/add_task.html"
    context = {}

    def get(self, request):
        if self.request.user.is_teacher:
            user_id = self.request.user.id
            form = ChooseStudentForm(user_id=user_id)
            self.context["form"] = form
            return render(request, self.template_name, self.context)
        return HttpResponse('Error')

    def post(self, request):
        student_id = request.POST.get('user')
        return redirect(f'add_task/{student_id}')


class AddTaskView(View):
    template_name = "tasks/add_task.html"
    context = {}

    def get(self, request, pk):
        if self.request.user.is_teacher:
            kits = TaskList.objects.get(user_id=pk)
            form = AddTaskForm(instance=kits)
            self.context["form"] = form
            return render(request, self.template_name, self.context)
        return HttpResponse('Error')

    def post(self, request, pk):
        kits = TaskList.objects.get(user_id=pk)
        form = AddTaskForm(data=request.POST, instance=kits)
        if form.is_valid():
            form.save()
            return HttpResponse('OK')
        return HttpResponse('Error')
