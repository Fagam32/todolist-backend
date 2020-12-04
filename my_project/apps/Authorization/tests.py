import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class AuthorizationApiTestCase(APITestCase):

    def test_registration(self):

        url = 'http://localhost:8000/auth/registration/'
        data = {"name": "dqwVasa", "surname": "fqwqwd2r1kin", "email": "laz@inbox.com", "password": "wwfwqed12rs4"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(email=data['email'], first_name=data['name'], last_name=data['surname']).exists())

    def test_authorize(self):
        url1 = 'http://localhost:8000/auth/registration/'
        data = {"name": "dqwVasa", "surname": "fqwqwd2r1kin", "email": "laz@inbox.com", "password": "Tester12345"}
        self.client.post(url1, data, format='json')
        user = User.objects.get(email=data['email'])
        data = {"email": "laz@inbox.com", "password": "Tester12345"}
        url = 'http://localhost:8000/auth/login/'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(json.loads(response.content))['token'].split()[1], Token.objects.get_or_create(user=user)[0].key)
