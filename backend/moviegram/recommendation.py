from django.contrib.auth.models import User
from moviegram.models import Movie, Rate
import pandas as pd
import numpy as np
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
    # users_df = pd.DataFrame(list(users.values()))
    movies_df = pd.DataFrame(list(movies.values()))
    ratings_df = pd.DataFrame(list(ratings.values()))

    user_ids = ratings_df["user_id"].unique().tolist()
    user2user_encoded = {x: i for i, x in enumerate(user_ids)}
    # userencoded2user = {i: x for i, x in enumerate(user_ids)}

    movie_ids = ratings_df["movie_id"].unique().tolist()
    movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
    movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}

    ratings_df["user_encoded"] = ratings_df["user_id"].map(user2user_encoded)
    ratings_df["movie_encoded"] = ratings_df["movie_id"].map(
        movie2movie_encoded)

    num_users = len(user2user_encoded)
    num_movies = len(movie_encoded2movie)

    # Min and max ratings will be used to normalize the ratings later
    min_rating = min(ratings_df["rate"])
    max_rating = max(ratings_df["rate"])

    print(
        f"Number of users: {num_users}, Number of Movies: {num_movies}, Min Rating: {min_rating}, Max Rating: {max_rating}")

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

    history = model.fit(
        x=x_train,
        y=y_train,
        batch_size=64,
        epochs=5,
        validation_data=(x_val, y_val)
    )

    # Get the movies watched by the user
    movies_watched_by_user = [
        rating.movie_id for rating in ratings if rating.user_id == user_id]

    # Find movies not watched by the user
    movies_not_watched = [
        movie_id for movie_id in movie_ids if movie_id not in movies_watched_by_user]

    # Convert to movie encoded format
    movies_not_watched_encoded = [
        movie2movie_encoded[movie_id] for movie_id in movies_not_watched]

    user_encoder = user2user_encoded[user_id]
    user_movie_array = np.full((len(movies_not_watched_encoded), 2), user_encoder)
    user_movie_array[:, 1] = movies_not_watched_encoded

    ratings_final = model.predict(user_movie_array).flatten()
    top_ratings_indices = ratings_final.argsort()[-10:][::-1]

    # Get recommended movie IDs
    recommended_movie_ids = [movie_encoded2movie[x] for x in top_ratings_indices] 

    # print("\nTop 10 recommended movie IDs:", recommended_movie_ids)

    # # Print recommendations
    # print("\nShowing recommendations for user: {}".format(user_id))
    # print("====" * 9)
    # print("Top 10 movie recommendations")
    # print("----" * 8)
    # # recommended_movies = movies_df[movies_df["id"].isin(recommended_movie_ids)]
    
    # # # for movie in recommended_movies.itertuples():
    # # #     cur_movie = Movie.objects.get(id=movie.id)
    # # #     genres_list = [genre.name for genre in cur_movie.genres.all()]
    # # #     print(movie.name, ":", genres_list, ":", movie.average_rating)

    return recommended_movie_ids
