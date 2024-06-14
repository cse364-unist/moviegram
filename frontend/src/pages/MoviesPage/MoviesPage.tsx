import React, {useEffect, useState} from 'react'; 


const MoviesPage = () => {
    const [movies, setMovies] = useState([]); 

    useEffect(() => {
        const fetchMovies = async () => {
            try{
                const response = await fetch('https://mooviegram-4860c7f65aef.herokuapp.com/movies')

                if(!response.ok){
                    throw new Error('Something went wrong')
                }
                const jsonMovies = await response.json() 
                setMovies(jsonMovies.results) // results is the key in the json object 
            }catch (error){
                console.log('Error fetching movies', error) 
            }
        }
        fetchMovies()
    }, [])

    return (
        <div>
            <h1 className='text-3xl font-bold text-center mt-10'>Movies</h1>
            <div className='grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4'>
                {movies.map((movie) => {
                    return (
                        <div key={movie.id} className='bg-white p-4 rounded-lg shadow-md'>
                            <h2 className='text-lg font-bold'>{movie.name}</h2>
                            <button className='bg-blue-500 text-white px-4 py-2 rounded-md mt-2'>View</button>
                        </div>
                    )
                })}
            </div>
        </div>

    )
}

export default MoviesPage 