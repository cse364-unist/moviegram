import React, { useState, useEffect } from 'react';

interface Movie {
  id: number;
  name: string;
  average_rating: number;
  review_list: any[]; // Adjust based on your actual data structure
  genres_list: any[]; // Adjust based on your actual data structure
  total_people_rated: number;
}

const ExplorePage: React.FC = () => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [canFetch, setCanFetch] = useState<boolean>(true); // Flag to control fetching
  const token = localStorage.getItem('token');

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      // const response = await fetch('http://localhost:8000/recommend/', {
      const response = await fetch('https://mooviegram-4860c7f65aef.herokuapp.com/recommend/', {
        headers: {
          Authorization: `Token ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }

      const data = await response.json();
      setMovies(data); // Assuming data is an array of Movie objects

      // Prevent fetching for the next 1 minute (60000 milliseconds)
      setCanFetch(false);
      setTimeout(() => setCanFetch(true), 60000); // Enable fetching after 1 minute
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      // Handle error state or show a message to the user
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const handleRefresh = () => {
    if (canFetch) {
      fetchRecommendations();
    } else {
      console.log('Please wait before refreshing again.'); // Optional: Provide feedback to the user
    }
  };

  return (
    <div className="container mx-auto py-8 px-48">
      <div className="text-center mb-6 mt-20">
        <h2 className="text-2xl font-semibold text-gray-600">
          Recommendations based on your preferences
        </h2>
      </div>
      <div className="flex justify-between items-center mb-6">
        <button
          onClick={handleRefresh} 
          className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600"
        >
          Refresh
        </button>
      </div>
      {loading ? (
        <div className="text-center text-gray-600">
          Loading our machine learning model. Please wait...
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6 justify-center">
          {movies.map((movie) => (
            <div key={movie.id} className="bg-white shadow-md rounded-lg overflow-hidden">
              <div className="p-4">
                <h2 className="text-xl font-bold mb-2">{movie.name}</h2>
                <p className="text-gray-600">
                  Average Rating: {movie.average_rating}
                </p>
                <div>
                  <h3>Genres:</h3>
                  <ul>
                    {movie.genres_list.map((genre, index) => (
                      <li key={index}>{genre}</li> 
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ExplorePage;