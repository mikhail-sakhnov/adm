import uuid
from django.shortcuts import redirect
from django import http
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, ProcessFormView
from users.forms import AdmUserForm, SubmitForm, ControlForm
from users.models import AdmUser, CurrentStatusModel


class IndexView(CreateView):
    template_name = "index.html"
    model = AdmUser
    form_class = AdmUserForm
    success_url = "token/"

    def get(self, request, *args, **kwargs):
        # Call the base implementation first to get a context
        is_active = CurrentStatusModel.objects.filter(
            is_active=True).count() >= 1

        if is_active:
            return redirect("search")
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url + self.object.token


class SeeYouView(TemplateView):
    template_name = "see.html"

    def get_context_data(self, **kwargs):
        context = super(SeeYouView, self).get_context_data(**kwargs)
        context['token'] = self.kwargs['token']
        return context


class StatusView(TemplateView):
    template_name = "status.html"
    model = CurrentStatusModel

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(StatusView, self).get_context_data(**kwargs)
        context['is_active'] = self.model.objects.filter(
            is_active=True).count() >= 1
        return context


class FindByTokenView(FormView):
    template_name = "token.html"
    form_class = SubmitForm

    def get_success_url(self):
        token = self.get_form().data['token']
        return "/token/{0}".format(token)


class TokenControlView(DetailView, ProcessFormView):
    model = AdmUser
    form = ControlForm
    slug_field = "token"
    template_name = "token_control.html"

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            return redirect("/")
        mode = form.cleaned_data['mode']
        if mode == "sent":
            obj = self.get_object()
            obj.sent = True
            obj.save()
            return redirect("/token/{0}".format(self.get_object().token))
        if mode == "leave":
            self.get_object().delete()
            return redirect("/")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(TokenControlView, self).get_context_data(**kwargs)
        context['is_active'] = CurrentStatusModel.objects.filter(
            is_active=True).count() >= 1
        return context
