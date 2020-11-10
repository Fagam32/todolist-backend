from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    text = models.TextField(max_length=200)
    isDone = models.BooleanField()
    creationDate = models.DateTimeField()
    lastUpdate = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
