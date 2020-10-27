from django.shortcuts import render
from django.views import View
import json
from datetime import datetime

from django.http import JsonResponse, Http404
from .models import Todo


class ToDoList(View):

    def get(self, request, *args, **kwargs):  # done
        return JsonResponse(list(Todo.objects.filter().values()), safe=False)  # костыль

    def post(self, request, *args, **kwargs):  # done
        time = datetime.now().replace(microsecond=0)
        todo = json.loads(request.body)
        temp = Todo(text=todo['text'], isDone=False, creationDate=time, lastUpdate=time)
        temp.save()
        return JsonResponse(list(Todo.objects.filter(creationDate=time).values()), safe=False)  # костыль

    def put(self, request, *args, **kwargs):  # done
        todo = json.loads(request.body)
        try:
            todo_from_db = Todo.objects.get(id=todo['id'])
            todo_from_db.text = todo['text']
            todo_from_db.isDone = todo['isDone']
            todo_from_db.lastUpdate = datetime.now().replace(microsecond=0)
            todo_from_db.save()
            return JsonResponse(list(Todo.objects.filter(id=todo['id']).values()))  # костыль
        except Todo.DoesNotExist:
            return Http404()

    def delete(self, request, *args, **kwargs):  # done
        todo = json.loads(request.body)
        try:
            Todo.objects.get(id=todo['id']).delete()
            return JsonResponse(True, safe=False)
        except Todo.DoesNotExist:
            return JsonResponse(False, safe=False)
