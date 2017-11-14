import uuid
from django.db import models


class AdmUser(models.Model):

    def get_default_token():
        return str(uuid.uuid4())
    full_name = models.CharField(max_length=300)
    full_address = models.TextField()
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100, default=get_default_token)


class CurrentStatusModel(models.Model):
    is_active = models.BooleanField()
