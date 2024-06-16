import React, { useState } from 'react';
import myImage from '../../../public/images/toy-story.jpg';

export default function MovieCard({ name, genres_list, average_rating, total_people_rated, id, review_list }) {
    const [reviewInput, setReviewInput] = useState('');
    const [reviews, setReviews] = useState(review_list); // Initialize with the prop value
    console.log('reviews:', reviews)

    const handleReviewInputChange = (e) => {
        setReviewInput(e.target.value);
    };

    const handleSubmitReview = async () => {
        if (reviewInput.trim() === '') {
            alert('Please enter a review.');
            return;
        }

        try {
            const response = await fetch(`http://localhost:8000/movies/${id}/review/`, {
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
            const newReview = await response.json();
            setReviews([...reviews, newReview]);
            setReviewInput('');
        } catch (error) {
            console.error('Error submitting review:', error);
            alert('Failed to submit review. Please try again.');
        }
    };

    return (
        <div className="w-full shadow-md shadow-black rounded-lg mt-8">
            <p className="text-center font-bold text-xl">{name}</p>
            <img className="mt-4 mx-auto rounded-lg" src={myImage} alt='Movie Poster' style={{ width: '250px', height: '350px' }} />

            <div className="px-6 py-4">
                <p className="font-bold text-md mt-4">Genres:</p>
                <ul className="text-sm">
                    {genres_list.map(genre => (
                        <li key={genre.id}>{genre.name}</li>
                    ))}
                </ul>
            </div>

            <div className="px-6 py-4">
                <p className="font-bold text-md">Rating: {average_rating}</p>
                <p className="font-bold text-md">Rated by: {total_people_rated}</p>
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
                    className="w-full border rounded-lg p-2 focus:outline-none"
                    placeholder="Write your review..."
                    value={reviewInput}
                    onChange={handleReviewInputChange}
                ></textarea>
                <button onClick={handleSubmitReview} className="bg-blue-500 text-white px-4 py-2 rounded-md mt-2 hover:bg-blue-600 focus:outline-none">
                    Submit Review
                </button>
            </div>
        </div>
    );
}
