import json

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from app_user.models import User


class MovieSimpleTests(APITestCase):
    def setUp(self):
        pass

    def test_list(self):
        # data = {
        # }
        # response = self.client.post('/api/movie/simple/', data, format='json')
        # # print(response.data)
        # self.assertNotEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = '123123'
        json.loads(data)
