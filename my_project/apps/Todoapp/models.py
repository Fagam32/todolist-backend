from django.db import models

# my_id = models.IntegerField()
class Todo(models.Model):
    text = models.TextField(max_length=200)
    isDone = models.BooleanField()
    creationDate = models.DateTimeField()
    lastUpdate = models.DateTimeField()
