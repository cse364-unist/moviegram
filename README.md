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
Step 2: Login to your newly created account  
From now on you are going to use this username and password in each request you make. Because there functionalities that require the user to be authenticated.   

Step 3: Get the users list to follow  
```bash
curl -X GET http://localhost:8000/users/ | json_pp
```  

Step 4: Follow a user  
```bash
curl -X POST -u username:password http://localhost:8000/follow/<user_id>/ | json_pp
```

Step 5: Get the movie list  
Following request return first 100 movie items out of 3883 movies. As it has pagination enabled.  
```bash 
curl -X GET http://localhost:8000/movies/ | json_pp
```

Step 6: Give a rating to a movie from 1 to 5 
```bash

```

Step 7: Leave a review to a movie  
Step 8: Save a movie to your favorites  
Step 9: Share your activities with followers (they will see it on their feed)  
Step 10: Take a look at friends activities from the feed  


### Feature #2: Movie Collections - Makida
This feature helps users to (1) create collections of movies and (2) follow other collections of movies that were created by other users. Similar to Spotify music collections. Each time creator of collection adds new movie then all the followers are notifed on a new movie.  
Below are the API endpoints that are supported.   

1. Get the list of collections (we will have some preadded collections) 
2. Choose the collection and see the movies that it has 
3. Follow a collection 
4. Create your own collection
5. Add a new movie to your collection 


### Feature #3: Movie Recommendations - Aizat 
The purpose of this feature is to help users to explore new movies to watch. Our recommendation system uses collaborative recommendation, that is to recommend movies based on the movies that were watched by friends of the user.  
Make a GET request to following endpoint by providing authentication credentials.  
```bash
curl -u username:password  http://localhost:8000/recommend/ | json_pp
``` 

Below is the request to get recommendations for our user that we created.
```bash
curl -u instructor:asdf  http://localhost:8000/recommend/ | json_pp
```  
