from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Movie, Rate, Review, Collection 

import random 

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

    # TO DO: Fix this test case. Error is raised from recommend endpoint. 
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
        user_1 = User.objects.create_user(username='user1', password='asdf')
        user_2 = User.objects.create_user(username='user2', password='asdf')
        cls.user_1_id = user_1.id 
        cls.user_2_id = user_2.id 

    def setUp(self):
        self.client = APIClient()

    def test_successfull_follow_attempt(self):
        user = User.objects.get(username='user1')
        self.client.force_authenticate(user=user)

        response = self.client.post(
            reverse('user-follow', kwargs={'user_id': self.user_2_id}))
        self.assertEqual(response.status_code, 201)

    def test_unauthenticated_follow_attempt(self):
        response = self.client.post(
            reverse('user-follow', kwargs={'user_id': self.user_2_id}))
        self.assertEqual(response.status_code, 401)

    def test_non_existing_user_follow_attempt(self):

        user = User.objects.get(username='user1')
        self.client.force_authenticate(user=user)

        non_exist_id = random.randint(1000, 10000)
        try: 
            non_user = User.objects.get(id=non_exist_id)
            while non_user:
                non_exist_id = random.randint(1000, 10000)
                non_user = User.objects.get(id=non_exist_id)
        except ObjectDoesNotExist:
            response = self.client.post(
                reverse('user-follow', kwargs={'user_id': non_exist_id}))
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


class GetMovieAPITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create_user(
            username='staff', password='asdf', is_staff=True)
        user_2 = User.objects.create_user(username='nonstaff', password='asdf')
        movie_1 = Movie.objects.create(name='BlaBlaShow_1')
        movie_2 = Movie.objects.create(name='BlaBlaShow_2')
        cls.movie_1_id = movie_1.id
        cls.movie_2_id = movie_2.id

    def setUp(self):
        self.client = APIClient()

    def test_successfull_status(self):
        response = self.client.get(reverse('movie-list'))

        self.assertEqual(response.status_code, 200)

    def test_correct_response_data(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    def test_successfull_status_detail_view(self):
        response = self.client.get(
            reverse('movie-detail', kwargs={'pk': self.movie_1_id}))
        self.assertEqual(response.status_code, 200)

    def test_unsuccessful_status_detail_view(self):
        response = self.client.get(reverse('movie-detail', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, 404)

    def test_successfull_post_new_movie(self):
        user = User.objects.get(username='staff')
        self.client.force_authenticate(user=user)

        movie_data = {'name': 'blablashow'}
        response = self.client.post(
            reverse('movie-list'), movie_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_unauthorized_post_new_movie(self):
        user = User.objects.get(username='nonstaff')
        self.client.force_authenticate(user=user)

        movie_data = {'name': 'blablashow'}
        response = self.client.post(
            reverse('movie-list'), movie_data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_successfull_delete_movie(self):
        user = User.objects.get(username='staff')
        self.client.force_authenticate(user=user)

        response = self.client.delete(
            reverse('movie-detail', kwargs={'pk': self.movie_2_id}))
        self.assertEqual(response.status_code, 204)

    def test_unauthorized_delete_movie(self):
        user = User.objects.get(username='nonstaff')
        self.client.force_authenticate(user=user)

        response = self.client.delete(
            reverse('movie-detail', kwargs={'pk': self.movie_2_id}))
        self.assertEqual(response.status_code, 403)

    def test_successfull_update_movie(self):
        user = User.objects.get(username='staff')
        self.client.force_authenticate(user=user)
        movie_data = {'name': 'UpdatedName'}

        response = self.client.put(
            reverse('movie-detail', kwargs={'pk': self.movie_2_id}), movie_data, format='json')
        self.assertEqual(response.status_code, 200)
        update_movie = Movie.objects.get(id=self.movie_2_id)
        update_movie_name = update_movie.name
        self.assertEqual(update_movie_name, movie_data['name'])

    def test_unauthorized_update_movie(self):
        user = User.objects.get(username='nonstaff')
        self.client.force_authenticate(user=user)
        movie_data = {'name': 'UpdatedName'}

        response = self.client.put(
            reverse('movie-detail', kwargs={'pk': self.movie_2_id}), movie_data, format='json')
        self.assertEqual(response.status_code, 403)


class RateMovieAPITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create_user(
            username='user1', password='asdf', is_staff=True)
        user_2 = User.objects.create_user(username='user2', password='asdf')

        movie_1 = Movie.objects.create(name='BlaBlaShow_1')
        movie_2 = Movie.objects.create(name='BlaBlaShow_2')
        cls.movie_1_id = movie_1.id
        cls.movie_2_id = movie_2.id

    def setUp(self):
        self.client = APIClient()

    def test_successfull_rate(self):
        user = User.objects.get(username="user1")
        self.client.force_authenticate(user=user)

        rate_data = {'rating': 2}
        response = self.client.post(reverse(
            'movie-rate', kwargs={'movie_id': self.movie_1_id}), rate_data, format='json')
        self.assertEqual(response.status_code, 201)

        rate_count = Rate.objects.count()
        self.assertEqual(rate_count, 1)

        movie = Movie.objects.get(id=self.movie_1_id)
        movie_rate = movie.average_rating
        self.assertEqual(movie_rate, 2)

    def test_unauthorized_rate_attempt(self):
        rate_data = {'rating': 2}
        response = self.client.post(reverse(
            'movie-rate', kwargs={'movie_id': self.movie_1_id}), rate_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_non_existing_movie_rate_attempt(self):
        user = User.objects.get(username="user1")
        self.client.force_authenticate(user=user)
        
        non_exist_movie_id = 10000
        movie = Movie.objects.filter(id=non_exist_movie_id).first()
        self.assertIsNone(movie)

        rate_data = {'rating': 2}
        response = self.client.post(reverse(
            'movie-rate', kwargs={'movie_id': non_exist_movie_id}), rate_data, format='json')
        self.assertEqual(response.status_code, 404)

        rate_count = Rate.objects.count()
        self.assertEqual(rate_count, 0)


class ReviewMovieAPITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create_user(
            username='user1', password='asdf', is_staff=True)
        user_2 = User.objects.create_user(username='user2', password='asdf')

        movie_1 = Movie.objects.create(name='BlaBlaShow_1')
        movie_2 = Movie.objects.create(name='BlaBlaShow_2')
        cls.movie_1_id = movie_1.id
        cls.movie_2_id = movie_2.id

    def setUp(self):
        self.client = APIClient()

    def test_successfull_review(self):
        user = User.objects.get(username="user1")
        self.client.force_authenticate(user=user)

        review = {'content': "I love BlaBlaShow. "}
        response = self.client.post(reverse(
            'movie-review', kwargs={'movie_id': self.movie_1_id}), review, format='json')
        self.assertEqual(response.status_code, 201)

        review_count = Review.objects.count()
        self.assertEqual(review_count, 1)

    def test_unauthorized_review_attempt(self):
        review = {'content': "I love BlaBlaShow. "}
        response = self.client.post(reverse(
            'movie-review', kwargs={'movie_id': self.movie_1_id}), review, format='json')
        self.assertEqual(response.status_code, 401)

    def test_non_existing_movie_review_attempt(self):
        user = User.objects.get(username="user1")
        self.client.force_authenticate(user=user)

        non_exist_movie_id = 10000
        movie = Movie.objects.filter(id=non_exist_movie_id).first()
        self.assertIsNone(movie)

        review = {'content': "I love BlaBlaShow. "}
        response = self.client.post(reverse(
            'movie-review', kwargs={'movie_id': non_exist_movie_id}), review, format='json')
        self.assertEqual(response.status_code, 404)

        rate_count = Rate.objects.count()
        self.assertEqual(rate_count, 0)


class FeedAPITest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create_user(
            username='user1', password='asdf', is_staff=True)
        user_2 = User.objects.create_user(username='user2', password='asdf')

        movie_1 = Movie.objects.create(name='BlaBlaShow_1')
        movie_2 = Movie.objects.create(name='BlaBlaShow_2')
        cls.movie_1_id = movie_1.id
        cls.movie_2_id = movie_2.id

    def setUp(self):
        self.client = APIClient()

    def test_successfull_feed_response(self):
        user = User.objects.get(username='user1')
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('feed'))

        self.assertEqual(response.status_code, 200)
    
    def test_unauthorized_feed_attempt(self): 
        response = self.client.get(reverse('feed')) 
        
        self.assertEqual(response.status_code, 401) 

class CollectionAPITest(TestCase): 

    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create_user(
            username='user1', password='asdf', is_staff=True)

        movie_1 = Movie.objects.create(name='BlaBlaShow_1')
        movie_2 = Movie.objects.create(name='BlaBlaShow_2')
  
        cls.movie_1_id = movie_1.id
        cls.movie_2_id = movie_2.id

        collection_1 = Collection.objects.create(name='Funny movies', user=user_1, is_public=True)
        cls.collection_1_id = collection_1.id 

        collection_2 = Collection.objects.create(name='Sad movies', user=user_1)
        cls.collection_2_id = collection_2.id 
    def setUp(self):
        self.client = APIClient()
    
    def test_successfull_collection_retrieve(self): 
        response = self.client.get(reverse('collection-list'))
        self.assertEqual(response.status_code, 200) 
    
    def test_public_collection_detail(self): 
        # Test existing collection 
        response = self.client.get(reverse('collection-detail', kwargs={'pk':self.collection_1_id}))
        self.assertEqual(response.status_code, 200) 

        # Test non-existing collection 
        non_exist_collection_id = 10000 
        response_2 = self.client.get(reverse('collection-detail', kwargs={'pk':non_exist_collection_id}))  
        self.assertEqual(response_2.status_code, 404) 

    def test_non_public_collection_detail(self): 
        response = self.client.get(reverse('collection-detail', kwargs={'pk':self.collection_2_id}))
        self.assertEqual(response.status_code, 403)  

        user = User.objects.get(username='user1') 
        self.client.force_authenticate(user=user) 
        response_2 = self.client.get(reverse('collection-detail', kwargs={'pk':self.collection_2_id})) 
        self.assertEqual(response_2.status_code, 200) 
    
class FollowCollectionAPITest(TestCase): 

    @classmethod 
    def setUpTestData(cls): 
        user_1 = User.objects.create_user(
            username='user1', password='asdf')

        movie_1 = Movie.objects.create(name='BlaBlaShow_1')
        movie_2 = Movie.objects.create(name='BlaBlaShow_2')
  
        cls.movie_1_id = movie_1.id
        cls.movie_2_id = movie_2.id

        collection_1 = Collection.objects.create(name='Funny movies', user=user_1, is_public=True)
        cls.collection_1_id = collection_1.id 

        collection_2 = Collection.objects.create(name='Sad movies', user=user_1)
        cls.collection_2_id = collection_2.id 
    def setUp(self):
        self.client = APIClient() 

    def test_collection_follow_attempt(self): 
        user = User.objects.get(username='user1') 
        self.client.force_authenticate(user=user) 

        response = self.client.post(reverse('collection-follow', kwargs={'collection_id':self.collection_1_id}))
        self.assertEqual(response.status_code, 200) 

        non_exist_collection_id = 10000
        response_2 = self.client.post(reverse('collection-follow', kwargs={'collection_id':non_exist_collection_id}))
        self.assertEqual(response_2.status_code, 404) 
    
        response_3 = self.client.post(reverse('collection-follow', kwargs={'collection_id':self.collection_1_id}))
        self.assertEqual(response_3.status_code, 409) 

    
    def test_unauthorized_follow(self): 
        response = self.client.post(reverse('collection-follow', kwargs={'collection_id':self.collection_1_id}))
        self.assertEqual(response.status_code, 401) 
    
class UnfollowCollectionAPITest(TestCase): 

    @classmethod
    def setUpTestData(cls): 
        user_1 = User.objects.create_user(
            username='user1', password='asdf')

        movie_1 = Movie.objects.create(name='BlaBlaShow_1')
        movie_2 = Movie.objects.create(name='BlaBlaShow_2')
  
        cls.movie_1_id = movie_1.id
        cls.movie_2_id = movie_2.id

        collection_1 = Collection.objects.create(name='Funny movies', user=user_1, is_public=True)
        cls.collection_1_id = collection_1.id 

        collection_2 = Collection.objects.create(name='Sad movies', user=user_1)
        cls.collection_2_id = collection_2.id 
    
    def setUp(self):
        self.client = APIClient()  

    def test_collection_unfollow_attempt(self): 
        user = User.objects.get(username='user1') 
        self.client.force_authenticate(user=user) 

        response = self.client.post(reverse('collection-follow', kwargs={'collection_id':self.collection_1_id}))
        self.assertEqual(response.status_code, 200) 

        response_2 = self.client.post(reverse('collection-unfollow', kwargs={'collection_id':self.collection_1_id}))
        self.assertEqual(response_2.status_code, 200)

        response_3 = self.client.post(reverse('collection-unfollow', kwargs={'collection_id':self.collection_1_id}))
        self.assertEqual(response_3.status_code, 409)

        non_exist_collection_id = 10000
        response_4 = self.client.post(reverse('collection-unfollow', kwargs={'collection_id':non_exist_collection_id}))
        self.assertEqual(response_4.status_code, 404)


    def test_unauthorized_unfollow(self): 
        response = self.client.post(reverse('collection-unfollow', kwargs={'collection_id':self.collection_1_id}))
        self.assertEqual(response.status_code, 401)     

class CreateCollectionAPITest(TestCase): 

    @classmethod
    def setUpTestData(cls): 
        user_1 = User.objects.create_user(
            username='user1', password='asdf')
  
        cls.collection_data = {}

        movie_1 = Movie.objects.create(name='BlaBlaShow_1')
        movie_2 = Movie.objects.create(name='BlaBlaShow_2')
  
        cls.movie_1_id = movie_1.id
        cls.movie_2_id = movie_2.id
    
    def setUp(self):
        self.client = APIClient()  

    def test_unauthorized_collection_create(self): 
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json') 
        self.assertEqual(response.status_code, 401) 
    
    
    def test_successfull_collection_create(self): 
        user = User.objects.get(username='user1')
        self.client.force_authenticate(user=user) 

        response = self.client.post(reverse('collection-list'), self.collection_data, format='json') 
        self.assertEqual(response.status_code, 400) 

        self.collection_data['name'] = "Very funny movies" 
        
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json') 
        self.assertEqual(response.status_code, 400)  

        self.collection_data['is_public'] = 'True' 
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json') 
        self.assertEqual(response.status_code, 200)  

        self.collection_data['movies'] = [10] 
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json') 
        self.assertEqual(response.status_code, 400) 

        self.collection_data['movies'] = [self.movie_1_id] 
        response = self.client.post(reverse('collection-list'), self.collection_data, format='json') 
        self.assertEqual(response.status_code, 200) 

class AddMovieToCollectionTest(TestCase): 
    @classmethod
    def setUpTestData(cls): 
        user_1 = User.objects.create_user(
            username='user1', password='asdf')
        user_2 = User.objects.create_user(
            username='user2', password='asdf')
  
        collection_1 = Collection.objects.create(name="Funny movies collection", user_id=user_1.id)
        cls.collection_1_id = collection_1.id 

        movie_1 = Movie.objects.create(name='BlaBlaShow_1')
        movie_2 = Movie.objects.create(name='BlaBlaShow_2')
  
        cls.movie_1_id = movie_1.id
        cls.movie_2_id = movie_2.id
    
    def setUp(self):
        self.client = APIClient() 

    def test_unauthorized_add(self): 
        response = self.client.post(reverse('collection-add', kwargs={'collection_id':self.collection_1_id}))
        self.assertEqual(response.status_code, 401) 
    
    def test_add_movie_to_collection(self): 
        user = User.objects.get(username = 'user2') 
        self.client.force_authenticate(user=user) 

        non_existing_collection_id = 10000 
        response = self.client.post(reverse('collection-add', kwargs={'collection_id':non_existing_collection_id}))
        self.assertEqual(response.status_code, 404)

        response_2 = self.client.post(reverse('collection-add', kwargs={'collection_id':self.collection_1_id}))
        self.assertEqual(response_2.status_code, 403)  
    
    def test_successfull_add_movie_to_collection(self): 
        user = User.objects.get(username = 'user1') 
        self.client.force_authenticate(user=user) 

        response = self.client.post(reverse('collection-add', kwargs={'collection_id':self.collection_1_id}))
        self.assertEqual(response.status_code, 400) 

        request_data = {'movie':"hi"} 
        response_2 = self.client.post(reverse('collection-add', kwargs={'collection_id':self.collection_1_id}), request_data, format='json')
        self.assertEqual(response_2.status_code, 400)

        non_exist_movie_id = 10000
        request_data = {'movie':non_exist_movie_id} 
        response_3 = self.client.post(reverse('collection-add', kwargs={'collection_id':self.collection_1_id}), request_data, format='json')
        self.assertEqual(response_3.status_code, 404) 

        request_data = {'movie':self.movie_1_id} 
        response_4 = self.client.post(reverse('collection-add', kwargs={'collection_id':self.collection_1_id}), request_data, format='json')
        self.assertEqual(response_4.status_code, 200) 

        


