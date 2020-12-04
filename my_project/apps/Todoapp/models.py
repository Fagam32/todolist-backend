from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    text = models.TextField(max_length=200)
    isDone = models.BooleanField(null=True)
    creationDate = models.DateTimeField(null=True)
    lastUpdate = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
