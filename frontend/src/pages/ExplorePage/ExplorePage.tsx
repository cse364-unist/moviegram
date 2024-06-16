import React, { useState } from 'react';

interface Movie {
  id: number;
  title: string;
  rating: number;
  imageUrl: string;
  genres: string;
}

const ExplorePage: React.FC = () => {
  const initialMovies: Movie[] = [
    {
      id: 1,
      title: "Inception",
      rating: 8.8,
      imageUrl: "https://image.tmdb.org/t/p/w500/qmDpIHrmpJINaRKAfWQfftjCdyi.jpg",
      genres: "Action, Sci-Fi",
    },
    {
      id: 2,
      title: "The Dark Knight",
      rating: 9.0,
      imageUrl: "https://image.tmdb.org/t/p/w500/1hRoyzDtpgMU7Dz4JF22RANzQO7.jpg",
      genres: "Action, Crime, Drama",
    },
    {
      id: 3,
      title: "Interstellar",
      rating: 8.6,
      imageUrl: "https://image.tmdb.org/t/p/w500/rAiYTfKGqDCRIIqo664sY9XZIvQ.jpg",
      genres: "Adventure, Drama, Sci-Fi",
    },
    {
      id: 4,
      title: "The Matrix",
      rating: 8.7,
      imageUrl: "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
      genres: "Action, Sci-Fi",
    },
    {
      id: 5,
      title: "Gladiator",
      rating: 8.5,
      imageUrl: "https://image.tmdb.org/t/p/w500/ty8TGRuvJLPUmAR1H1nRIsgwvim.jpg",
      genres: "Action, Adventure, Drama",
    },
    {
      id: 6,
      title: "The Godfather",
      rating: 9.2,
      imageUrl: "https://image.tmdb.org/t/p/w500/rSPw7tgCH9c6NqICZef4kZjFOQ5.jpg",
      genres: "Crime, Drama",
    },
    {
      id: 7,
      title: "Pulp Fiction",
      rating: 8.9,
      imageUrl: "https://image.tmdb.org/t/p/w500/tGpTpVyIow4NzHVsxyA1A8EIVdd.jpg",
      genres: "Crime, Drama",
    },
    {
      id: 8,
      title: "Fight Club",
      rating: 8.8,
      imageUrl: "https://image.tmdb.org/t/p/w500/bptfVGEQuv6vDTIMVCHjJ9Dz8PX.jpg",
      genres: "Drama",
    },
    {
      id: 9,
      title: "Forrest Gump",
      rating: 8.8,
      imageUrl: "https://image.tmdb.org/t/p/w500/yE5d3BUhE8hCnkMUJOo1QDoOGNz.jpg",
      genres: "Drama, Romance",
    },
    {
      id: 10,
      title: "The Shawshank Redemption",
      rating: 9.3,
      imageUrl: "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
      genres: "Drama",
    },
  ];


  const [movies, setMovies] = useState<Movie[]>(initialMovies);

  const refreshMovies = () => {
    const newMovies: Movie[] = [
      {
        id: 11,
        title: "Avengers: Endgame",
        rating: 8.4,
        imageUrl: "https://image.tmdb.org/t/p/w500/ulzhLuWrPK07P1YkdWQLZnQh1JL.jpg",
        genres: "Action, Adventure, Drama",
      },
      {
        id: 12,
        title: "Titanic",
        rating: 7.8,
        imageUrl: "https://image.tmdb.org/t/p/w500/kHXEpyfl6zqn8a6YuozZUujufXf.jpg",
        genres: "Drama, Romance",
      },
      // Add more movies here...
    ];
    setMovies(newMovies);
  };


  return (
    <div className="container mx-auto py-8 px-48">
      <h1 className="text-3xl font-bold mb-8 text-center">Explore</h1>
      <div className="text-center mb-6">
        <h2 className="text-2xl font-semibold text-gray-600">Recommendations based on your preferences</h2>
      </div>
      <div className="flex justify-between items-center mb-6">
        <div></div> {}
        <button
          onClick={refreshMovies}
          className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600"
        >
          Refresh
        </button>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6 justify-center">
        {movies.map((movie) => (
          <div key={movie.id} className="bg-white shadow-md rounded-lg overflow-hidden">
            <img
              src={movie.imageUrl}
              alt={movie.title}
              className="w-full h-64 object-cover"
            />
            <div className="p-4">
              <h2 className="text-xl font-bold mb-2">{movie.title}</h2>
              <p className="text-gray-600">{movie.genres}</p>
              <p className="text-gray-800 font-semibold">Rating: {movie.rating}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ExplorePage;
