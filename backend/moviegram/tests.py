from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from django.contrib.auth.models import User


class UserCreationAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'instructor',
            'email': 'myemail@example.com',
            'password': 'asdf'
        }
        self.auth_data = {
            'username': 'instructor',
            'password': 'asdf'
        }

    def test_user_creation_endpoint(self):

        # Send a POST request to the endpoint
        response = self.client.post(
            reverse('user-list'), self.user_data, format='json')

        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Assert that a user with the given username exists in the database
        self.assertTrue(User.objects.filter(username='instructor').exists())

    #TO DO: this test is not working. Don't know why? Must figure out later. 
    # def test_user_authentication(self):
    #     client = APIClient()
    #     user_data = {
    #         'username': 'instructor',
    #         'email': 'myemail@example.com',
    #         'password': 'asdf'
    #     }

    #     # Create a new user
    #     client.post(reverse('user-list'), user_data, format='json')
    #     self.assertTrue(User.objects.filter(username='instructor').exists())

    #     # Authenticate with basic authentication
    #     print(">>", client.login(username='instructor', password='asdf'))

    #     # Send a GET request to a protected endpoint (example)
    #     response = client.get(reverse('recommend-list'))

    #     # Assert that the response status code is 200 (OK)
    #     self.assertEqual(response.status_code, 200)
