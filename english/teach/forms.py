from django import forms
from teach.models import Kit, Card


class TranslateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TranslateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'custom_input'

    translate_word = forms.CharField(label="Перевод", max_length=100, required=False)


class CreateKitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Kit
        exclude = (
            Kit.user.field.name,
        )


class CreateCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Card
        exclude = (
            Card.user.field.name,
        )
