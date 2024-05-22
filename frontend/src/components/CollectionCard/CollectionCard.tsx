import './CollectionCard.css'; // Assuming you have the CSS file from the previous step
import darkKnightPoster from '../../../public/images/dark_knight.jpg'; // Import the image
import inceptionPoster from '../../../public/images/inception.jpg';
import madmaxPoster from '../../../public/images/mad_max.jpg';
import diehardPoster from '../../../public/images/die_hard.jpg';
// Import other images as needed

export default function CollectionCard() {
    // Sample movie data
    const movieCollections = [
        {
            title: "Action Movies",
            movies: [
                { title: "The Dark Knight", poster: darkKnightPoster },
                { title: "Inception", poster: inceptionPoster },
                { title: "Mad Max: Fury Road", poster: madmaxPoster },
                { title: "Die Hard", poster: diehardPoster }
            ]
        },
        {
            title: "Comedy Movies",
            movies: [
                { title: "Superbad", poster: "superbad.jpg" },
                { title: "The Hangover", poster: "hangover.jpg" },
                { title: "Dumb and Dumber", poster: "dumb_and_dumber.jpg" },
                { title: "Anchorman: The Legend of Ron Burgundy", poster: "anchorman.jpg" }
            ]
        },
        // Add more collections as needed
    ];

    return (
        <>
            <div className='test'>
                {movieCollections.map((collection, index) => (
                    <div className='card' key={index}>
                        <h2>{collection.title}</h2>
                        <div className='movies'>
                            {collection.movies.slice(0, 4).map((movie, movieIndex) => (
                                <div className='movie' key={movieIndex}>
                                    <img src={movie.poster} alt={movie.title} />
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </>
    )
}