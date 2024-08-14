from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from django.views.generic.edit import FormMixin
from teach.models import Card, Kit
import random
from teach.forms import TranslateForm, CreateKitForm, CreateCardForm


class DontRepeat:
    previous_ids = []

    def a(self, id):
        self.previous_ids.append(id)

    def r(self):
        del self.previous_ids[0]

    def g(self):
        return self.previous_ids


pr_ids = DontRepeat


class Functions:
    def get_cards_kit_ids(self, kit_id):
        kit = Kit.objects.filter(id=kit_id)[0]
        ids = [el.id for el in kit.cards.all()]
        return ids

    def get_random_pk_from_kit(self, ids):
        card_id = random.choice(ids)
        return card_id


class StartView(View):
    template_name = "teach/start.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.method == 'POST':
            kit_pk = 1
            if request.method == 'POST':
                ids = Functions.get_cards_kit_ids(self, kit_pk)
                while True:
                    card_pk = Functions.get_random_pk_from_kit(self, ids)
                    if card_pk not in pr_ids.g(pr_ids):
                        pr_ids.a(pr_ids, card_pk)
                        break
                    if len(pr_ids.g(pr_ids)) > len(ids) - 1:
                        pr_ids.r(pr_ids)
                return redirect(f"/kit/{kit_pk}/card/{card_pk}/")


class CorrectlyView(View):
    template_name = "teach/correctly.html"

    def get(self, request, kit_pk, card_pk):
        return render(request, self.template_name)

    def post(self, request, kit_pk, card_pk):
        if request.method == 'POST':
            ids = Functions.get_cards_kit_ids(self, kit_pk)
            while True:
                card_pk = Functions.get_random_pk_from_kit(self, ids)
                if card_pk not in pr_ids.g(pr_ids):
                    pr_ids.a(pr_ids, card_pk)
                    break
                if len(pr_ids.g(pr_ids)) > len(ids) - 1:
                    pr_ids.r(pr_ids)
            return redirect(f"/kit/{kit_pk}/card/{card_pk}/")


class WrongView(View):
    template_name = "teach/wrong.html"
    context = {}

    def get(self, request, kit_pk, card_pk):
        old_post = self.request.session.get('_old_post')
        self.context['correct'] = old_post
        return render(request, self.template_name, self.context)

    def post(self, request, kit_pk, card_pk):
        if request.method == 'POST':
            ids = Functions.get_cards_kit_ids(self, kit_pk)
            while True:
                card_pk = Functions.get_random_pk_from_kit(self, ids)
                if card_pk not in pr_ids.g(pr_ids):
                    pr_ids.a(pr_ids, card_pk)
                    break
                if len(pr_ids.g(pr_ids)) > len(ids) - 1:
                    pr_ids.r(pr_ids)
            return redirect(f"/kit/{kit_pk}/card/{card_pk}/")


class KitDetailView(DetailView):
    template_name = "teach/kit_detail.html"
    context_object_name = 'kit_info'
    context = {}
    previous_ids = []

    def get(self, request, pk):
        return render(request, self.template_name, self.context)

    def post(self, request, pk):
        if request.method == 'POST':
            kit_pk = pk
            if request.method == 'POST':
                ids = Functions.get_cards_kit_ids(self, kit_pk)
                while True:
                    card_pk = Functions.get_random_pk_from_kit(self, ids)
                    if card_pk not in pr_ids.g(pr_ids):
                        pr_ids.a(pr_ids, card_pk)
                        break
                    if len(pr_ids.g(pr_ids)) > len(ids) - 1:
                        pr_ids.r(pr_ids)
                return redirect(f"/kit/{kit_pk}/card/{card_pk}/")


class KitsView(View):
    template_name = "teach/kits_list.html"
    context = {}

    def get(self, request):
        kits = Kit.objects.only(
            'name',
        )
        self.context['kits'] = kits
        return render(request, self.template_name, self.context)


class KitCardDetailView(View):
    template_name = "teach/detail.html"
    context_object_name = 'card_info'
    context = {}

    def get(self, request, kit_pk, card_pk):
        kit = Kit.objects.filter(id=kit_pk)[0]
        card = kit.cards.filter(id=card_pk)[0]
        self.context['card_info'] = card
        form = TranslateForm(request.POST)
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, kit_pk, card_pk):
        if request.method == 'POST':
            form = TranslateForm(request.POST)
            self.request.session['_old_post'] = str(self.context['card_info'].translation).split(', ')[0]
            if form.is_valid():
                if form.cleaned_data['translate_word'] in str(self.context['card_info'].translation).split(', '):
                    return redirect(f"/kit/{kit_pk}/card/{card_pk}/correctly/")
            return redirect(f"/kit/{kit_pk}/card/{card_pk}/wrong/")


class KitCreateView(View, FormMixin):
    template_name = "teach/create_kit.html"
    model = Kit
    context = {}
    form_class = CreateKitForm
    success_url = '/kits/'

    def get(self, request):
        if self.request.user.is_teacher:
            self.context["form"] = self.form_class()
            return render(request, self.template_name, self.context)
        else:
            return redirect('/warning_stuf')

    def post(self, request):
        if request.method == "POST":
            form = CreateKitForm(request.POST)
            if form.is_valid():
                form_save = form.save(commit=True)
                form_save.user = self.request.user
                form_save.save()
                return redirect(self.success_url)
        self.context["form"] = form
        return render(request, self.template_name, self.context)


class CardCreateView(View):
    template_name = "teach/create_card.html"
    model = Card
    context = {}
    form_class = CreateCardForm
    success_url = '/'

    def get(self, request):
        if self.request.user.is_teacher:
            self.context["form"] = self.form_class()
            return render(request, self.template_name, self.context)
        else:
            return redirect('/warning_stuf')

    def post(self, request):
        if request.method == "POST":
            form = CreateCardForm(request.POST)
            if form.is_valid():
                form_save = form.save(commit=False)
                form_save.user = self.request.user
                form_save.save()
                return redirect(self.success_url)
        self.context["form"] = form
        return render(request, self.template_name, self.context)


class WarningStufView(View):
    template_name = "teach/warning_stuf.html"

    def get(self, request):
        return render(request, self.template_name)


class MyKitsView(View):
    template_name = "teach/kits_list.html"
    context = {}

    def get(self, request):
        kits = Kit.objects.filter(user=self.request.user).only(
            'name',
        )
        self.context['kits'] = kits
        return render(request, self.template_name, self.context)


class AboutView(View):
    template_name = "teach/about.html"

    def get(self, request):
        return render(request, self.template_name)
