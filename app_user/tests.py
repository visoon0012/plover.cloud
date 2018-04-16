from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from app_user.models import User


class PublicTests(APITestCase):
    def test_register(self):
        """
        测试注册
        """
        data = {
            'username': 'A123456',
            'password': '123456',
            'email': 'A123456@qq.com',
        }
        response = self.client.post('/api/user/', data, format='json')
        print(response.data)
        users = User.objects.all()
        for user in users:
            print(user.__dict__)
        self.assertNotEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class UserTests(APITestCase):
    def setUp(self):
        # 创建一个用户
        # 创建用户
        self.user = User.objects.create(username='A123456', email='A123456@qq.com', password='123456')
        self.user.save()
        self.user2 = User.objects.create(username='B123456', email='B123456@qq.com', password='123456')
        self.user2.save()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_login(self):
        data = {
            'username': 'A123456',
            'password': '123456',
        }
        response = self.client.post('/api/token/auth/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user(self):
        data = {
            'username': 'A123456',
        }
        response = self.client.get('/api/user/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        data = {
            'username': 'A123456',
        }
        response = self.client.delete('/api/user/1/', data, format='json')
        print(response.data)

    def test_put_user(self):
        data = {
            'username': 'A123456',
            'like_times': 100,
        }
        response = self.client.put('/api/user/1/', data, format='json')
        print(response.data)

    def test_forgot_user(self):
        data = {
            'username': 'A123456',
            'password': '12345678',
            'email': 'A123456@qq.com',
        }
        response = self.client.put('/api/user/forgot/', data, format='json')
        print(response.data)
