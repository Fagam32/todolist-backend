from django.shortcuts import render
from django.views import View
import json
from datetime import datetime

from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, Http404
from .models import Todo


class ToDoList(View):

    def get(self, request, *args, **kwargs):  # done
        return JsonResponse(list(Todo.objects.filter().values()), safe=False) # костыль

    def post(self, request, *args, **kwargs):  # done
        time = datetime.now().replace(microsecond=0)
        get_inf = (json.loads(str(request.body, encoding='utf-8')))['currTodo']  # мб тоже костыль( надо ли приобразовывать к строке перед loads)
        temp = Todo(text=get_inf['text'], isDone=False, creationDate=time, lastUpdate=time)
        temp.save()
        return JsonResponse(list(Todo.objects.filter(creationDate=time).values()), safe=False)  # костыль

    def put(self, request, *args, **kwargs):  # done
        inf_for_update = (json.loads(str(request.body, encoding='utf-8')))['currTodo']
        try:
            todo_from_base = Todo.objects.get(id=inf_for_update['id'])
            todo_from_base.text = inf_for_update['text']
            todo_from_base.isDone = inf_for_update['isDone']
            todo_from_base.lastUpdate = datetime.now().replace(microsecond=0)
            todo_from_base.save()
            return JsonResponse(list(Todo.objects.filter(id=inf_for_update['id']).values()), safe=False)  # костыль
        except Todo.DoesNotExist:
            return Http404()

    def delete(self, request, *args, **kwargs):  # done
        inf_for_delete = (json.loads(str(request.body, encoding='utf-8')))['currTodo']  # мб тоже костыль( надо ли приобразовывать к строке перед loads)
        try:
            Todo.objects.get(id=inf_for_delete['id']).delete()
            return JsonResponse(True, safe=False)
        except Todo.DoesNotExist:
            return JsonResponse(False, safe=False)
