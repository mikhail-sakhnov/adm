import uuid
from django.db import models
from django.db.models.signals import post_save
from users.apps import UsersConfig
from django.dispatch import receiver


class AdmUser(models.Model):

    def get_default_token():
        return str(uuid.uuid4())
    full_name = models.CharField(max_length=300)
    full_address = models.TextField()
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100, default=get_default_token)
    sent = models.BooleanField(default=False)


class CurrentStatusModel(models.Model):
    is_active = models.BooleanField()


@receiver(post_save, sender=AdmUser, dispatch_uid="new_adm_user")
def on_new_user_created(sender, instance, **kwargs):
    if AdmUser.objects.all().count() >= UsersConfig.users_for_start:
        status = CurrentStatusModel.objects.filter(is_active=False).first()
        if status:
            status.is_active = True
            status.save()


@receiver(post_save, sender=CurrentStatusModel, dispatch_uid="status_changed")
def on_status_changed(sender, instance, **kwargs):
    if AdmUser.objects.all().count() >= UsersConfig.users_for_start:
        pass  # start_adm()
    else:
        status = CurrentStatusModel.objects.filter(is_active=True).first()
        if status:
            status.is_active = False
            status.save()
