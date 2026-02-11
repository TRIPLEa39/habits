from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_created = models.DateField(default=timezone.now)
    