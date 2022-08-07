from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    es_secretaria = models.BooleanField(default=False)
    es_medico = models.BooleanField(default=False)
    es_taller = models.BooleanField(default=False)
    es_ventas = models.BooleanField(default=False)
    es_gerencia = models.BooleanField(default=False)

    class Meta:
        db_table = "auth_user"
