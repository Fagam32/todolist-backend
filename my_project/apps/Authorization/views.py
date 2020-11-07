from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.db.utils import IntegrityError

class Registration(View):

    def post(self, request, *args, **kwargs):
        getting_data = json.loads(request.body)
        try:
            User.objects.create(username=getting_data['email'], first_name=getting_data['name'], last_name=getting_data['surname'],
                                email=getting_data['email'], password=getting_data['password'])
            return JsonResponse("", safe=False, status=200)
        except IntegrityError:  # если какой-то параметр не уникален
            return JsonResponse("", safe=False, status=404)
