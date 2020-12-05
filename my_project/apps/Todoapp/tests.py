import json
from datetime import datetime

# from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Todo


class TodoApiTestCase(APITestCase):

    def setUpTestData(cls=APITestCase):  # fix: must setUpTestData(cls)???
        user = User.objects.create(username='tester', password='test12345')
        Token.objects.create(user=user)
        time = datetime.now().replace(microsecond=0)
        for i in range(5):
            Todo.objects.create(user=user, text='First tdo', isDone=False, creationDate=time, lastUpdate=time)

    def test_get(self):
        user = User.objects.get(id=1)
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='TOKEN ' + token.key)
        url = 'http://localhost:8000/todos/'  # настроить автогенерацию через reverse(django.urls)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, JsonResponse(list(Todo.objects.all().values()), safe=False).content)  # fix

    def test_post(self):
        user = User.objects.get(id=1)
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='TOKEN ' + token.key)
        url = 'http://localhost:8000/todos/'  # настроить автогенерацию через reverse(django.urls)
        todo = {"text": "added todo", "isDone": False}
        response = self.client.post(url, todo, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Todo.objects.filter(text=todo['text'], isDone=todo['isDone']).exists())

    def test_put(self):
        user = User.objects.get(id=1)
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='TOKEN ' + token.key)
        url = 'http://localhost:8000/todos/'  # настроить автогенерацию через reverse(django.urls)
        todo = {"id": 2, "text": "updated todo", "isDone": True}
        response = self.client.put(url, todo, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(json.loads(response.content) is None)

    def test_delete(self):
        user = User.objects.get(id=1)
        token = Token.objects.get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='TOKEN ' + token.key)
        url = 'http://localhost:8000/todos/'  # настроить автогенерацию через reverse(django.urls)
        todo = {"id": 3}
        response = self.client.delete(url, todo, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(json.loads(response.content))  # успешно ли удаление


class TodoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Todo.objects.create(text='Todo for test')

    def test_text_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')

    def test_isDone_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('isDone').verbose_name
        self.assertEquals(field_label, 'isDone')

    def test_creationDate_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('creationDate').verbose_name
        self.assertEquals(field_label, 'creationDate')

    def test_lastUpdate_label(self):
        todo = Todo.objects.get(id=1)
        field_label = todo._meta.get_field('lastUpdate').verbose_name
        self.assertEquals(field_label, 'lastUpdate')

    def test_text_max_length(self):
        todo = Todo.objects.get(id=1)
        max_length = todo._meta.get_field('text').max_length
        self.assertEquals(max_length, 200)
