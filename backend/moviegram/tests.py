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
        '''
        Test successfull user creation.
        '''

        # Send a POST request to the endpoint
        response = self.client.post(
            reverse('user-list'), self.user_data, format='json')

        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Assert that a user with the given username exists in the database
        self.assertTrue(User.objects.filter(username='instructor').exists())

    def test_duplicate_user_creation(self):
        '''
        Test whether duplicate usernames are not allowed.
        '''
        # Send a POST request to the endpoint
        response = self.client.post(
            reverse('user-list'), self.user_data, format='json')

        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Create another user with the same username
        response = self.client.post(
            reverse('user-list'), self.user_data, format='json')

        self.assertEqual(response.status_code, 400)

    # def test_user_authentication(self):
    #     '''
    #     Make a request to a protected enpoint.
    #     '''
    #     client = APIClient()
    #     user_data = {
    #         'username': 'instructor',
    #         'email': 'myemail@example.com',
    #         'password': 'asdf'
    #     }

    #     client.post(reverse('user-list'), user_data, format='json')
    #     user = User.objects.get(username='instructor')

    #     # Authenticate the client with the created user
    #     client.force_authenticate(user=user)

    #     # Make a GET request to the 'recommend-list' endpoint
    #     response = client.get(reverse('recommend-list'))

    #     # Assert that the response status code is 200 (OK)
    #     self.assertEqual(response.status_code, 200)


class UserListAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_successfull_status(self):
        response = self.client.get(reverse('user-list'))

        self.assertEqual(response.status_code, 200)

    def test_correct_response_data(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')


class FollowUserAPITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user1', password='asdf')
        User.objects.create_user(username='user2', password='asdf')

    def setUp(self):
        self.client = APIClient()

    def test_successfull_follow_attempt(self):
        user = User.objects.get(username='user1')
        self.client.force_authenticate(user=user)

        response = self.client.post(
            reverse('user-follow', kwargs={'user_id': 2}))
        self.assertEqual(response.status_code, 201)

    def test_unauthenticated_follow_attempt(self):
        response = self.client.post(
            reverse('user-follow', kwargs={'user_id': 1}))
        self.assertEqual(response.status_code, 401)

    def test_non_existing_user_follow_attempt(self):

        user = User.objects.get(username='user1')
        self.client.force_authenticate(user=user)

        response = self.client.post(
            reverse('user-follow', kwargs={'user_id': 3}))
        self.assertEqual(response.status_code, 404)


class UnfollowUserAPITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='user1', password='asdf')
        user2 = User.objects.create_user(username='user2', password='asdf')
        cls.user1_id = user1.id
        cls.user2_id = user2.id

    def setUp(self):
        self.client = APIClient()

    def test_successfull_unfollow_attempt(self):
        user = User.objects.get(username='user1')
        self.client.force_authenticate(user=user)
        self.client.post(
            reverse('user-follow', kwargs={'user_id': self.user2_id}))

        response = self.client.delete(
            reverse('user-unfollow', kwargs={'user_id': self.user2_id}))
        self.assertEqual(response.status_code, 200)

    def test_unfollow_not_following_attempt(self):
        user = User.objects.get(username='user1')
        self.client.force_authenticate(user=user)
        response = self.client.delete(
            reverse('user-unfollow', kwargs={'user_id': self.user2_id}))
        self.assertEqual(response.status_code, 404)
