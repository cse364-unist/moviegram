import React, { useEffect, useState } from 'react';
import MovieCard from '../../components/MovieCard/MovieCard';

interface Movie {
    id: number;
    name: string;
    genres_list: { id: number; name: string }[];
    average_rating: number;
    total_people_rated: number;
    review_list: { id: number; user_name: string; content: string }[];
    // Add other properties as needed based on your API response
}

const MoviesPage: React.FC = () => {
    const [movies, setMovies] = useState<Movie[]>([]);

    useEffect(() => {
        const fetchMovies = async () => {
            try {
                const response = await fetch('https://mooviegram-4860c7f65aef.herokuapp.com/movies');
                // const response = await fetch('http://localhost:8000/movies');

                if (!response.ok) {
                    throw new Error('Something went wrong');
                }
                const jsonMovies = await response.json();
                setMovies(jsonMovies.results); // results is the key in the json object
            } catch (error) {
                console.log('Error fetching movies', error);
            }
        };
        fetchMovies();
    }, []);

    return (
        <div>
            <div className='grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4'>
                {movies?.map((movie) => (
                    <MovieCard {...movie} key={movie.id} />
                ))}
            </div>
        </div>
    );
};

export default MoviesPage;
