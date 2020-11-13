from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token


class Registration(View):

    def post(self, request, *args, **kwargs):
        getting_data = json.loads(request.body)
        # TODO remove password from cheсking on uniq
        try:
            User.objects.create_user(username=getting_data['email'], first_name=getting_data['name'],
                                     last_name=getting_data['surname'],
                                     email=getting_data['email'], password=getting_data['password'])
            return JsonResponse("", safe=False, status=200)
        except IntegrityError:  # если какой-то параметр не уникален

            return JsonResponse("", safe=False, status=400)


class Authorize(View):

    def post(self, request, *args, **kwargs):
        credentials = json.loads(request.body)
        user = authenticate(request, username=credentials['email'], password=credentials['password'])
        if user:
            token = Token.objects.get_or_create(user=user)
            response = {"roles": ["USER"], "token": "Bearer " + str(token[0])}
            return JsonResponse(response, safe=False, status=200)
        else:
            return JsonResponse("User no found", safe=False, status=404)
