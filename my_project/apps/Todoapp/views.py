import json
from datetime import datetime
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views import View
from rest_framework.authtoken.models import Token

from .models import Todo


def get_user(request):
    token = request.headers['Authorization']
    token = token.split()[1]
    user = Token.objects.get(key=token).user
    return user


class ToDoList(View):

    def get(self, request, *args, **kwargs):
        user = get_user(request)
        all_todos = list(Todo.objects.filter(user=user).values())  # убрать user_id
        return JsonResponse(all_todos, safe=False)

    def post(self, request, *args, **kwargs):
        time = datetime.now().replace(microsecond=0)
        todo = json.loads(request.body)
        user = get_user(request)
        temp = Todo(text=todo['text'], isDone=False, creationDate=time, lastUpdate=time, user=user)
        temp.save()
        added_todo = list(Todo.objects.filter(creationDate=time).values())
        return JsonResponse(added_todo, safe=False, status=201)

    def put(self, request, *args, **kwargs):
        todo = json.loads(request.body)
        try:
            todo_from_db = Todo.objects.get(id=todo['id'], user=get_user(request))
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
            Todo.objects.get(id=todo['id'], user=get_user(request)).delete()
            return JsonResponse(True, safe=False, status=200)
        except Todo.DoesNotExist:
            return JsonResponse(False, safe=False, status=404)
