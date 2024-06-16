import React, { useState } from 'react';
import myImage from '../../../public/images/toy-story.jpg';

interface Genre {
    id: number;
    name: string;
}

interface Review {
    id: number;
    user_name: string;
    content: string;
}

interface MovieCardProps {
    name: string;
    genres_list: Genre[];
    average_rating: number;
    total_people_rated: number;
    id: number;
    review_list: Review[];
}

const MovieCard: React.FC<MovieCardProps> = ({ name, genres_list, average_rating, total_people_rated, id, review_list }) => {
    const [reviewInput, setReviewInput] = useState<string>('');
    const [reviews, setReviews] = useState<Review[]>(review_list); // Initialize with the prop value
    const [userRating, setUserRating] = useState<number>(0);

    console.log('reviews:', reviews);

    const handleReviewInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setReviewInput(e.target.value);
    };

    const handleSubmitReview = async () => {
        if (reviewInput.trim() === '') {
            alert('Please enter a review.');
            return;
        }

        try {
            // const response = await fetch(`http://localhost:8000/movies/${id}/review/`, {
            const response = await fetch(`https://mooviegram-4860c7f65aef.herokuapp.com/movies/${id}/review/`, {
        
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Token ${localStorage.getItem('token')}`,
                },
                body: JSON.stringify({ content: reviewInput }),
            });

            if (!response.ok) {
                throw new Error('Failed to submit review');
            }
            const newReview: Review = await response.json();
            setReviews([...reviews, newReview]);
            setReviewInput('');
        } catch (error) {
            console.error('Error submitting review:', error);
            alert('Failed to submit review. Please try again.');
        }
    };

    const handleRatingChange = (rating: number) => {
        setUserRating(rating);
    };

    const handleSubmitRating = async () => {
        if (userRating < 1 || userRating > 5) {
            alert('Please select a rating between 1 and 5.');
            return;
        }

        try {
            // const response = await fetch(`http://localhost:8000/movies/${id}/rate/`, {
            const response = await fetch(`https://mooviegram-4860c7f65aef.herokuapp.com/movies/${id}/rate/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Token ${localStorage.getItem('token')}`,
                },
                body: JSON.stringify({ rating: userRating }),
            });

            if (!response.ok) {
                throw new Error('Failed to submit rating');
            }

            alert('Rating submitted successfully!');
        } catch (error) {
            console.error('Error submitting rating:', error);
            alert('Already rated the movie');
        }
    };

    const renderStars = (rating: number, interactive: boolean = false) => {
        const stars = [];
        const starStyle: React.CSSProperties = {
            width: '29.35px',
            height: '29.15px',
            fill: '#34A853',
            stroke: '#34A853',
            strokeWidth: '1',
            strokeLinejoin: 'round',
            cursor: interactive ? 'pointer' : 'default',
        };

        for (let i = 0; i < 5; i++) {
            stars.push(
                <svg
                    key={i}
                    style={starStyle}
                    viewBox="0 0 24 24"
                    onClick={interactive ? () => handleRatingChange(i + 1) : undefined}
                >
                    <polygon
                        points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"
                        fill={i < rating ? '#34A853' : 'none'}
                        stroke="#34A853"
                        strokeWidth="1"
                        strokeLinejoin="round"
                    />
                </svg>
            );
        }
        return stars;
    };

    return (
        <div className="w-full shadow-md rounded-lg mt-8 text-black" style={{ boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1), 0 6px 20px rgba(0, 0, 0, 0.1)' }}>
            <p className="text-center font-bold text-xl">{name}</p>
            
            <div className="flex justify-center">
                <img className="mt-4 mx-auto rounded-lg" src={myImage} alt='Movie Poster' style={{ width: '183.06px', height: '272px' }} />
            </div>

            <div className="px-6 py-4">
                <p className="font-bold text-md mt-4">Genres:</p>
                <p className="text-sm">{genres_list.map(genre => genre.name).join(', ')}</p>
            </div>

            <div className="px-6 py-4">
                <div className="flex items-center">
                    <div className="flex">
                        {renderStars(Math.round(average_rating))}
                    </div>
                    <p className="ml-4 font-bold text-md">Rated by: {total_people_rated}</p>
                </div>
                <div className="flex items-center mt-4">
                    <div className="flex">
                        {renderStars(userRating, true)}
                    </div>
                    <button onClick={handleSubmitRating} className="bg-gray-800 text-white px-4 py-2 rounded-md ml-4 hover:bg-gray-700 focus:outline-none" style={{ backgroundColor: '#292929' }}>
                        Submit Rating
                    </button>
                </div>
            </div>

            <div className="px-6 py-4">
                <p className="font-bold text-md">Reviews:</p>
                <ul className="text-sm">
                    {reviews.map(review => (
                        <li key={review.id}>
                            <strong>{review.user_name}</strong>: {review.content}
                        </li>
                    ))}
                </ul>
            </div>

            <div className="px-6 py-4">
                <textarea
                    className="w-full border border-purple-500 rounded-lg p-2 focus:outline-none bg-transparent"
                    placeholder="Write your review..."
                    value={reviewInput}
                    onChange={handleReviewInputChange}
                ></textarea>
                <button onClick={handleSubmitReview} className="bg-gray-800 text-white px-4 py-2 rounded-md mt-2 hover:bg-gray-700 focus:outline-none" style={{ backgroundColor: '#292929' }}>
                    Submit Review
                </button>
            </div>
        </div>
    );
};

export default MovieCard;
