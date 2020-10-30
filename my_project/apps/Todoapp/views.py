import json
from datetime import datetime

from django.http import JsonResponse
from django.views import View

from .models import Todo


class ToDoList(View):

    def get(self, request, *args, **kwargs):
        all_todos = list(Todo.objects.filter().values())
        return JsonResponse(all_todos, safe=False)

    def post(self, request, *args, **kwargs):
        time = datetime.now().replace(microsecond=0)
        todo = json.loads(request.body)
        temp = Todo(text=todo['text'], isDone=False, creationDate=time, lastUpdate=time)
        temp.save()
        added_todo = list(Todo.objects.filter(creationDate=time).values())
        return JsonResponse(added_todo, safe=False)

    def put(self, request, *args, **kwargs):
        todo = json.loads(request.body)
        try:
            todo_from_db = Todo.objects.get(id=todo['id'])
            todo_from_db.text = todo['text']
            todo_from_db.isDone = todo['isDone']
            todo_from_db.lastUpdate = datetime.now().replace(microsecond=0)
            todo_from_db.save()
            updated_todo = list(Todo.objects.filter(id=todo['id']).values())
            return JsonResponse(updated_todo, safe=False)
        except Todo.DoesNotExist:
            return JsonResponse(None, safe=False, status=404)

    def delete(self, request, *args, **kwargs):
        todo = json.loads(request.body)
        try:
            Todo.objects.get(id=todo['id']).delete()
            return JsonResponse(True, safe=False, status=200)
        except Todo.DoesNotExist:
            return JsonResponse(False, safe=False, status=404)
