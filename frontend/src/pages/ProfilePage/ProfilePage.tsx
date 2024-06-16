import React, { useState } from 'react';

interface UserProfile {
    username: string;
    profilePictureUrl: string;
    bio: string;
    followers: number;
    following: number;
}

interface Movie {
    title: string;
    rating: number;
}

interface Review {
    movieTitle: string;
    reviewText: string;
}

const ProfilePage: React.FC = () => {
    const [userProfile, setUserProfile] = useState<UserProfile>({
        username: 'JohnDoe',
        profilePictureUrl: '',
        bio: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
        followers: 1000,
        following: 500,
    });

    const movies: Movie[] = [
        { title: 'Inception', rating: 5 },
        { title: 'Interstellar', rating: 4 },
        { title: 'The Dark Knight', rating: 5 },
        { title: 'Fight Club', rating: 4 },
        { title: 'Pulp Fiction', rating: 5 },
    ];

    const reviews: Review[] = [
        { movieTitle: 'Inception', reviewText: 'Amazing movie with a mind-bending plot!' },
        { movieTitle: 'Interstellar', reviewText: 'A visually stunning and emotionally profound journey.' },
        { movieTitle: 'The Dark Knight', reviewText: 'The best Batman movie ever made.' },
        { movieTitle: 'Fight Club', reviewText: 'A cult classic with a brilliant twist.' },
        { movieTitle: 'Pulp Fiction', reviewText: 'A masterpiece of nonlinear storytelling.' },
    ];

    const [isEditing, setIsEditing] = useState<boolean>(false);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];

        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setUserProfile({
                    ...userProfile,
                    profilePictureUrl: reader.result as string,
                });
            };
            reader.readAsDataURL(file);
        }
    };

    const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const { name, value } = event.target;
        setUserProfile((prevProfile) => ({
            ...prevProfile,
            [name]: value,
        }));
    };

    const handleSave = () => {
        setIsEditing(false);
        // Save the updated profile data to the server or local storage
    };

    return (
        <div className="flex flex-col justify-center items-center min-h-screen pt-24 text-black">
            <div className="bg-white w-full max-w-screen-lg shadow-lg rounded-lg overflow-hidden mb-8">
                <div className="px-6 py-4">
                    <div className="flex items-center mb-4">
                        <label htmlFor="profile-picture" className="relative">
                            <div className="relative group">
                                <div className="w-20 h-20 rounded-full overflow-hidden border-4 border-gray-300 shadow-lg flex items-center justify-center">
                                    {!userProfile.profilePictureUrl && (
                                        <svg
                                            xmlns="http://www.w3.org/2000/svg"
                                            viewBox="0 0 448 512"
                                            className="w-12 h-12 text-gray-400"
                                        >
                                            <path d="M224 256A128 128 0 1 0 224 0a128 128 0 1 0 0 256zm-45.7 48C79.8 304 0 383.8 0 482.3C0 498.7 13.3 512 29.7 512H418.3c16.4 0 29.7-13.3 29.7-29.7C448 383.8 368.2 304 269.7 304H178.3z" />
                                        </svg>
                                    )}
                                    {userProfile.profilePictureUrl && (
                                        <img
                                            className="w-full h-full object-cover"
                                            src={userProfile.profilePictureUrl}
                                            alt="Profile"
                                        />
                                    )}
                                    <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 group-hover:opacity-100">
                                        <p className="text-white text-sm">Change Picture</p>
                                    </div>
                                </div>
                                <input
                                    id="profile-picture"
                                    type="file"
                                    accept=".jpg, .jpeg, .png"
                                    className="hidden"
                                    onChange={handleFileChange}
                                />
                            </div>
                        </label>
                        <div className="ml-4 flex-1">
                            {isEditing ? (
                                <>
                                    <input
                                        type="text"
                                        name="username"
                                        value={userProfile.username}
                                        onChange={handleChange}
                                        className="block w-full mb-2 p-2 border border-gray-300 rounded"
                                    />
                                    <div className="flex justify-between text-sm text-gray-600 mb-2">
                                        <p>Followers: {userProfile.followers}</p>
                                        <p>Following: {userProfile.following}</p>
                                    </div>
                                    <textarea
                                        name="bio"
                                        value={userProfile.bio}
                                        onChange={handleChange}
                                        className="block w-full mb-2 p-2 border border-gray-300 rounded"
                                    />
                                    <button
                                        className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded"
                                        onClick={handleSave}
                                    >
                                        Save
                                    </button>
                                </>
                            ) : (
                                <>
                                    <h2 className="text-xl font-bold">{userProfile.username}</h2>
                                    <div className="flex justify-between text-sm text-gray-600 mb-2">
                                        <p>Followers: {userProfile.followers}</p>
                                        <p>Following: {userProfile.following}</p>
                                    </div>
                                    <p className="text-sm text-gray-600 mb-2">Bio: {userProfile.bio}</p>
                                    <button
                                        className="bg-yellow-500 hover:bg-yellow-600 text-white py-2 px-4 rounded"
                                        onClick={() => setIsEditing(true)}
                                    >
                                        Edit Profile
                                    </button>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </div>
            <div className="bg-white w-full max-w-screen-lg shadow-lg rounded-lg overflow-hidden mb-8">
                <div className="px-6 py-4">
                    <h3 className="text-xl font-bold mb-4">Recently Rated Movies</h3>
                    <ul>
                        {movies.map((movie, index) => (
                            <li key={index} className="mb-2">
                                <span className="font-bold">{movie.title}</span>: {movie.rating} stars
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
            <div className="bg-white w-full max-w-screen-lg shadow-lg rounded-lg overflow-hidden">
                <div className="px-6 py-4">
                    <h3 className="text-xl font-bold mb-4">Recent Reviews</h3>
                    <ul>
                        {reviews.map((review, index) => (
                            <li key={index} className="mb-2">
                                <span className="font-bold">{review.movieTitle}</span>: {review.reviewText}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;
