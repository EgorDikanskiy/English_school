from django import forms
from tasks.models import TaskList
from users.models import Teacher


class AddTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "custom_input"
        self.fields['kits'].widget.attrs.update({'class': 'custom_input cards_input'})

    class Meta:
        model = TaskList
        fields = (
            TaskList.kits.field.name,
        )


class ChooseStudentForm(forms.ModelForm):
    def __init__(self, user_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "custom_input"
        if user_id:
            queryset = Teacher.objects.get(pk=user_id).students.all()
            self.fields['user'].queryset = queryset

    class Meta:
        model = TaskList
        fields = (
            TaskList.user.field.name,
        )
