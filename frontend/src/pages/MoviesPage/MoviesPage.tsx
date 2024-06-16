import React, { useEffect, useState } from 'react'; 
import MovieCard from '../../components/MovieCard/MovieCard';

const MoviesPage = () => {
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
    console.log(movies)

    return (
        <div>
            <div className='grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4'>
                {movies?.map((movie) => (
                    <MovieCard {...movie} key={movie.id} />
                ))}
            </div>
        </div>
    )
}

export default MoviesPage;
