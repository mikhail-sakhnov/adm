import uuid
from django.shortcuts import redirect
from django import http
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from users.forms import AdmUserForm, SubmitForm
from users.models import AdmUser, CurrentStatusModel
from users.apps import UsersConfig


class IndexView(CreateView):
    template_name = "index.html"
    model = AdmUser
    form_class = AdmUserForm
    success_url = "see-you-later"

    def get(self, request, *args, **kwargs):
        # Call the base implementation first to get a context
        is_active = CurrentStatusModel.objects.filter(
            is_active=True).count() >= 1

        if is_active:
            return redirect("submit")
        return super(IndexView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        resp = super(IndexView, self).form_valid(form)
        if self.model.objects.all().count() >= UsersConfig.users_for_start:
            status = CurrentStatusModel.objects.all().first()
            status.is_active = True
            status.save()
        return resp


class SeeYouView(TemplateView):
    template_name = "see.html"


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
