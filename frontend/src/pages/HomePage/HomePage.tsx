import React, { useEffect, useState } from 'react';
import MovieCard from '../../components/MovieCard/MovieCard';

interface Movie {
    id: number;
    name: string;
    genres_list: [];
    average_rating: number;
    total_people_rated: number;
    review_list: [];
}

const HomePage: React.FC = () => {
    const [movies, setMovies] = useState<Movie[]>([]);

    useEffect(() => {
        const fetchMovies = async () => {
            try {
                // const response = await fetch('http://localhost:8000/movies');
                const response = await fetch('https://mooviegram-4860c7f65aef.herokuapp.com/movies');

                if (!response.ok) {
                    throw new Error('Something went wrong');
                }
                const jsonMovies = await response.json();
                setMovies(jsonMovies.results); // Assuming results is the key in the JSON object
            } catch (error) {
                console.log('Error fetching movies', error);
            }
        };
        fetchMovies();
    }, []);

    return (
        <div className="flex w-70 pt-16">
            <div className="w-20"> </div>
            <div className="w-60">
                {movies?.map((movie) => (
                    <MovieCard {...movie} key={movie.id} />
                ))}
            </div>
            <aside className="w-20"></aside>
        </div>
    );
};

export default HomePage;
