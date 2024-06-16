import React, { useEffect, useState } from 'react';
import MovieCard from '../../components/MovieCard/MovieCard';

const HomePage = () => {
    const [movies, setMovies] = useState([]);

    useEffect(() => {
        const fetchMovies = async () => {
            try {
                // const response = await fetch('https://mooviegram-4860c7f65aef.herokuapp.com/movies');
                const response = await fetch('http://localhost:8000/movies');

                if (!response.ok) {
                    throw new Error('Something went wrong');
                }
                const jsonMovies = await response.json();
                setMovies(jsonMovies.results); // results is the key in the json object 
            } catch (error) {
                console.log('Error fetching movies', error);
            }
        }
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
    )
}

export default HomePage;
