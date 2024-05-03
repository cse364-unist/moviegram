# Welcome!
# This is MovieGram - social media for movie lovers. 

## Note
If you don't have README previwer, please, open this README in the some previewer such as (https://markdownlivepreview.com/) for better experience.  

### Setup Instructions  
### Feature #1: Social Media notion
The purpose of this feature is to give an ability to users interact with each other as well as with movies. Collections of small features make up this big feature. To make sure users can interact with each other we implemented functinalities:  
1. Create a user. 
2. Follow other users. 
3. Rate movies. 
4. Review movies. 
5. Save movies to favorites.  
6. Share your activities with followers. 
7. See friends activities on the feed.  

Below is the detailed guide on how to test these functionalities.  
Assume that this is your first time opening our webpage.  
Let's register a user account for you, so you have full experience.  

Step 1: Register a new user account.  
To create a new user make a post request to the following API endpoint by providing username, email and password in the body.  
```bash
curl -X POST http://localhost:8000/users/ -d "username=username&email=email@example.com&password=mypassword123"
```   

Below is an example that you can use directly:   
```bash
curl -X POST http://localhost:8000/users/ -d "username=instructor&email=myemail@example.com&password=asdf"
```
Expected output
```bash
{
  "id": 6042,
  "username": "instructor"
}
```

Step 2: Login to your newly created account  
From now on you are going to use this username and password in each request you make. Because there functionalities that require the user to be authenticated.   

Step 3: Get the users list to follow  
```bash
curl -X GET http://localhost:8000/users/ | json_pp
```  
Snippet of Expected output
```bash
    {
      "email" : "",
      "follower_list" : [],
      "following_list" : [],
      "id" : 6040,
      "username" : "mbass"
   },
   {
      "email" : "email@example.com",
      "follower_list" : [],
      "following_list" : [],
      "id" : 6041,
      "username" : "username"
   },
   {
      "email" : "myemail@example.com",
      "follower_list" : [],
      "following_list" : [],
      "id" : 6042,
      "username" : "instructor"
   }
```
Step 4: Follow a user  
```bash
curl -X POST -u username:password http://localhost:8000/users/<user_id>/follow/ | json_pp
```

Example: Let's follow a user with id = 1  

```bash
curl -X POST -u instructor:asdf http://localhost:8000/users/1/follow/ | json_pp
```
Expected output
```bash
    {
   "message" : "You now follow williammyers."
    }
```

Reguest to unfollow a user:  
```bash
curl -X DELETE  -u username:password http://localhost:8000/users/<user_id>/unfollow/ | json_pp
```

Example: Let's unfollow a user with id = 1
```bash
curl -X DELETE -u instructor:asdf http://localhost:8000/users/1/unfollow/ | json_pp
```
Expected output
```bash
{
   "message" : "You have unfollowed williammyers."
}
```

Step 5: Get the movie list  
We enabled pagination for this request since our movie table has more 3000 movies. It returns 10 items per page, so it more comfortable to see the in the terminal when you check. You will get link to another page, so you can make another request to that page to get another 10 items.  
```bash 
curl -X GET http://localhost:8000/movies/ | json_pp
```
Expected output
```bash
{
   "count" : 3883,
   "next" : "http://localhost:8000/movies/?page=2",
   "previous" : null,
   "results" : [
      {
         "average_rating" : 4,
         "id" : 1,
         "name" : "Toy Story (1995)",
         "review_list" : [],
         "url" : "http://localhost:8000/movies/1/"
      },
      {
         "average_rating" : 3,
         "id" : 2,
         "name" : "Jumanji (1995)",
         "review_list" : [],
         "url" : "http://localhost:8000/movies/2/"
      },
      {
         "average_rating" : 3,
         "id" : 3,
         "name" : "Grumpier Old Men (1995)",
         "review_list" : [],
         "url" : "http://localhost:8000/movies/3/"
      },
      {
         "average_rating" : 2,
         "id" : 4,
         "name" : "Waiting to Exhale (1995)",
         "review_list" : [],
         "url" : "http://localhost:8000/movies/4/"
      },
      {
         "average_rating" : 3,
         "id" : 5,
         "name" : "Father of the Bride Part II (1995)",
         "review_list" : [],
         "url" : "http://localhost:8000/movies/5/"
      },
      {
         "average_rating" : 3,
         "id" : 6,
         "name" : "Heat (1995)",
         "review_list" : [],
         "url" : "http://localhost:8000/movies/6/"
      },
      {
         "average_rating" : 3,
         "id" : 7,
         "name" : "Sabrina (1995)",
         "review_list" : [],
         "url" : "http://localhost:8000/movies/7/"
      },
      {
         "average_rating" : 3,
         "id" : 8,
         "name" : "Tom and Huck (1995)",
         "review_list" : [],
         "url" : "http://localhost:8000/movies/8/"
      },
      {
         "average_rating" : 2,
         "id" : 9,
         "name" : "Sudden Death (1995)",
         "review_list" : [],
         "url" : "http://localhost:8000/movies/9/"
      },
      {
         "average_rating" : 3,
         "id" : 10,
         "name" : "GoldenEye (1995)",
         "review_list" : [],
         "url" : "http://localhost:8000/movies/10/"
      }
   ]
}
```
GET details of the single movie item by movie id:  
```bash 
curl -X GET http://localhost:8000/movies/<movie_id>/ | json_pp
``` 
Example: Get the details of movie #1 
```bash
curl -X GET http://localhost:8000/movies/1/ | json_pp
```
Expected output 
```bash
{
   "average_rating" : 4,
   "id" : 1,
   "name" : "Toy Story (1995)",
   "review_list" : [],
   "url" : "http://localhost:8000/movies/1/"
}
```

POST a new movie item. Only staff users have permissions.     
```bash
curl -X POST -u username:password -H "Content-Type: application/json" -d '{"name":"Movie Name"}' http://localhost:8000/movies/ | json_pp
```  
DELETE a movie item. Only staff users have permissions.  
```bash 
curl -X DELETE -u username:password http://localhost:8000/movies/1/
```
PUT (update) a movie item by id. Only staff users have permissions.  
```bash
curl -X PUT -u username:password -H "Content-Type: application/json" -d '{"name": "Updated Movie Name"}' http://localhost:8000/movies/3884/ | json_pp
```

Step 6: Give a rating to a movie from 1 to 5  
```bash
curl -X POST -u instructor:asdf -H "Content-Type: application/json" -d '{"rating": <given_rating>}' http://localhost:8000/movies/<movie_id>/rate/ | json_pp
```

Example command to give a rating 2 to a movie with id 1:   
 ```bash
 curl -X POST -u instructor:asdf -H "Content-Type: application/json" -d '{"rating": 2}' http://localhost:8000/movies/1/rate/ | json_pp
 ```

Step 7: Leave a review to a movie  
```bash
curl -X POST -u username:password -H "Content-Type: application/json" -d '{"content": "Your review text"}' http://localhost:8000/movies/<movie_id>/review/ | json_pp
```

Example command to leave a review to movie with id = 3.  
```bash
curl -X POST -u Instructor:asdf -H "Content-Type: application/json" -d '{"content": "I like this movie very much."}' http://localhost:8000/movies/3/review/ | json_pp
```
Expected output 
```bash
{
   "content" : "I like this movie very much.",
   "id" : 1,
   "movie" : 3,
   "user" : 6042
}
```
Step 8: Save a movie to your favorites  

Step 9: Take a look at friends activities from the home page (feed)    
```bash 
curl -X GET -u username:password http://localhost:8000/ | json_pp
```

Example request to get the your friends activity  
```bash
curl -X GET -u Instructor:asdf http://localhost:8000/ | json_pp
```
Expected output 
```bash
{
   "activities" : []
}
```


### Feature #2: Movie Collections
This feature helps users to (1) create collections of movies and (2) follow other collections of movies that were created by other users. Similar to Spotify music collections. Each time creator of collection adds new movie then all the followers are notifed on a new movie.  
Below are the API endpoints that are supported.   

1. Get the list of collections that already exist:   
```bash
curl -X GET http://localhost:8000/collections/ | json_pp
``` 
Expected output 
```bash
{
   "count" : 0,
   "next" : null,
   "previous" : null,
   "results" : []
}
```
2. Choose the collection and see the movies that it has 
```bash
curl -X GET http://localhost:8000/collections/<id>/ | json_pp
```
GET the details about collection with id = 1 (public collection):  
```bash
curl -X GET http://localhost:8000/collections/1/ | json_pp
```
Expected output 
```bash
{
   "detail" : "Not found."
}
```
To get the details about private collection authentications as a creator of collections is needed:  
```bash
curl -X GET -u username:password http://localhost:8000/collections/<id>/
```

3. Follow/Unfollow  a collection by collection id:  
```bash
curl -X POST -u username:password http://localhost:8000/collections/<id>/follow/
```
Example: Let's follow a collection with id = 1:  
```bash
curl -X POST -u instructor:asdf http://localhost:8000/collections/1/follow/ | json_pp
```
Expected output 
```bash
{
   "error" : "Collection is not found or not public. Please provide an existing public collection to follow."
}
```
```bash
curl -X POST -u username:password http://localhost:8000/collections/<id>/unfollow/
```
Example: Let's unfollow a collection with id = 1:  
```bash
curl -X POST -u instructor:asdf http://localhost:8000/collections/1/unfollow/ | json_pp
```

4. Create your own collection  
```bash
curl -X POST -u username:password -H "Content-type: application/json" -d '{"name" : "Collection Name", "is_public" : "True"}' http://localhost:8000/collections/
 ```

Example: Let's add a collection  
```bash
curl -X POST -u instructor:asdf -H "Content-type: application/json" -d '{"name" : "Funny movies", "is_public" : "True"}' http://localhost:8000/collections/
 ```
Expected output
```bash
{
"id":1,
"name": "Funny movies",
"user": 6042,
"is_public": true,
"movies_list": [],
"followers_list": []
}
```

5. Add a new movie to your collection 
```bash
curl -X POST -u username:password -H "Content-type: application/json" -d '{"movie":<movie_id>}' http://localhost:8000/collections/1/add/ | json_pp
```
Example: 
```bash
curl -X POST -u instructor:asdf -H "Content-type: application/json" -d '{"movie":"1"}' http://localhost:8000/collections/1/add/ | json_pp
```
Expected output 
```bash
{
   "message" : "Movie added to collection successfully."
}
```

### Feature #3: Movie Recommendations
Our recommendation feature utilizes collaborative filtering to provide personalized movie recommendations to users. This is how it works:

1. We preprocess the user, movie, and rating data. 
2. We train a neural network model using TensorFlow and Keras. The model learns embeddings for users and movies, capturing their latent features.
3. These embeddings are used to compute match scores between users and movies, incorporating user and movie biases.
4. We identify movies the user has not yet watched.
5. The model predicts ratings for these movies, and the top-rated movies are recommended to the user.

   
Make a GET request to the following endpoint by providing authentication credentials.  
```bash
curl -u username:password  http://localhost:8000/recommend/ | json_pp
``` 

Below is the request to get recommendations for our user that we created.
```bash
curl -u instructor:asdf  http://localhost:8000/recommend/ | json_pp
```  

## Test Coverage:  
Here is way to check for coverage: 
Assuming you are in the root directory.  
```bash
cd backend
coverage run manage.py test 
coverage report
```


## To do: 
1. Add some hyperlinking realtinoships in serializers. 
2. Add expected outcomes to the readme file 
3. 
