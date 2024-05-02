# from django.contrib.auth import get_user_model
# from moviegram.models import Movie, Rate

# User = get_user_model()
# users = [user.id for user in User.objects.all()]
# movies = [movie.id for movie in Movie.objects.all()]
# ratings = list(Rate.objects.all())

# def recommend_movies_for_user(user_id):
#     user = User.objects.get(id=user_id)  # current authenticated user
#     # ids of users that current user follows
#     followings_ids = [
#         following.following.id for following in user.following_set.all()]
#     username = user.get_username()

#     # case when the user does not follow others, just return the popular movies by rating
#     if len(followings_ids) == 0:
#         return "Popular movies"
#     # else return movie recommendations based on friends activity(friends' movie rates )
#     else:
#         return f'Below are the recommended movies for {username} (id = {user.id}) Based on his friends activity: {followings_ids}'


from django.contrib.auth.models import User
from moviegram.models import Movie, Rate
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from keras import Model, layers
import matplotlib.pyplot as plt


ratings = Rate.objects.all()
movies = Movie.objects.all()
users = User.objects.all()

EMBEDDING_SIZE = 50

class RecommenderNet(Model):
    def __init__(self, num_users, num_movies, embedding_size, **kwargs):
        super().__init__(**kwargs)
        self.num_users = num_users
        self.num_movies = num_movies
        self.embedding_size = embedding_size
        self.user_embedding = layers.Embedding(
            num_users,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.user_bias = layers.Embedding(num_users, 1)
        self.movie_embedding = layers.Embedding(
            num_movies,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6)
        )
        self.movie_bias = layers.Embedding(num_movies, 1)
        
    def call(self, inputs):
        user_vector = self.user_embedding(inputs[:, 0])
        user_bias = self.user_bias(inputs[:, 0])
        movie_vector = self.movie_embedding(inputs[:, 1])
        movie_bias = self.movie_bias(inputs[:, 1])
        dot_user_movie = tf.tensordot(user_vector, movie_vector, 2)
        # Add all the components (including bias)
        x = dot_user_movie + user_bias + movie_bias
        # The sigmoid activation forces the rating to be between 0 and 1
        return tf.nn.sigmoid(x)

def recommend_movies_for_user(user_id):
    users_df = pd.DataFrame(list(users.values()))
    movies_df = pd.DataFrame(list(movies.values()))
    ratings_df = pd.DataFrame(list(ratings.values()))


    # Map user ID to a "user vector" via an embedding matrix
    user_ids = ratings_df["user_id"].unique().tolist()
    user2user_encoded = {x: i for i, x in enumerate(user_ids)}
    userencoded2user = {i: x for i, x in enumerate(user_ids)}

    # Map movie ID to a "movie vector" via an embedding matrix
    movie_ids = ratings_df["movie_id"].unique().tolist()
    movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
    movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}

    ratings_df["user_encoded"] = ratings_df["user_id"].map(user2user_encoded)
    ratings_df["movie_encoded"] = ratings_df["movie_id"].map(movie2movie_encoded)

    num_users = len(user2user_encoded)
    num_movies = len(movie_encoded2movie)

    # Min and max ratings will be used to normalize the ratings later
    min_rating = min(ratings_df["rate"])
    max_rating = max(ratings_df["rate"])

    print(
        f"Number of users: {num_users}, Number of Movies: {num_movies}, Min Rating: {min_rating}, Max Rating: {max_rating}")


    #### Preparing the data####

    # Shuffling the data
    ratings_df = ratings_df.sample(frac=1, random_state=42)

    # Extracting features (user and movie IDs)
    x = ratings_df[["user_encoded", "movie_encoded"]].values

    # Normalizing the targets between 0 and 1
    y = ratings_df["rate"].apply(lambda x: (
        x - min_rating) / (max_rating - min_rating)).values

    # Splitting the data into training and validation sets
    x_train, x_val, y_train, y_val = train_test_split(
        x, y, test_size=0.1, random_state=42)

    # Check the shapes of the data to ensure correctness
    print("x_train shape:", x_train.shape)
    print("y_train shape:", y_train.shape)
    print("x_val shape:", x_val.shape)
    print("y_val shape:", y_val.shape)

    model = RecommenderNet(num_users, num_movies, EMBEDDING_SIZE)
    model.compile(
        loss=tf.keras.losses.BinaryCrossentropy(), optimizer=keras.optimizers.Adam(learning_rate=0.001)
    )

    ####Training the model on the Data Split####

    history = model.fit(
            x=x_train,
            y=y_train,
            batch_size=64,
            epochs=5,
            validation_data=(x_val, y_val)
        )

    # Plot training and validation loss
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    # Evaluate model on validation set
    loss = model.evaluate(x_val, y_val)
    print("Validation Loss:", loss)

    # Make predictions on validation set
    predictions = model.predict(x_val)

    # Inspect some sample predictions
    for i in range(5):
        print("Predicted Rating:", predictions[i][0])
        print("Actual Rating:", y_val[i])
        
    return "HI"

