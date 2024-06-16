import React, { useState, useEffect } from 'react';

export default function UsersPage() {
    const [users, setUsers] = useState([]);
    const currentUserId = parseInt(localStorage.getItem('user_id'), 10);
    const [followedby, setFollowedby] = useState([]);
    const [followingUsers, setFollowingUsers] = useState([]);

    console.log(followedby, followingUsers);

    useEffect(() => {

        const fetchUserDeails = async () => {
            try {
                const response = await fetch(`http://localhost:8000/users/${currentUserId}/`);
                if (!response.ok) {
                    throw new Error('Failed to fetch user details');
                }
                const data = await response.json();
                setFollowedby(data.follower_list);
                setFollowingUsers(data.following_list);
            }
            catch (error) {
                console.error('Error fetching user details:', error);
            }
        };

        const fetchUsers = async () => {
            try {
                const response = await fetch('http://localhost:8000/users/');
                if (!response.ok) {
                    throw new Error('Failed to fetch users');
                }
                const data = await response.json();
                setUsers(data.results); // Set the users state with the fetched data
            } catch (error) {
                console.error('Error fetching users:', error);
            }
        };

        fetchUserDeails();
        fetchUsers();
    }, []);

    async function handleFollow(userId) {
        try {
            const token = localStorage.getItem('token'); // Assuming you have a token stored in localStorage
            const response = await fetch(`http://localhost:8000/users/${userId}/follow/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
            });

            if (response.ok) {
                // Handle success, e.g., update UI or show success message
                console.log('Followed user successfully');
                setFollowingUsers(prevState => [...prevState, userId]);

            } else {
                // Handle failure, e.g., show error message
                console.error('Failed to follow user');
                alert('Failed to follow user');
            }
        } catch (error) {
            console.error('Error following user:', error);
            alert('Error following user. Please try again.');
        }
    }

    async function handleUnfollow(userId) {
        try {
            const token = localStorage.getItem('token'); // Assuming you have a token stored in localStorage
            const response = await fetch(`http://localhost:8000/users/${userId}/unfollow/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`
                },
            });

            if (response.ok) {
                // Handle success, e.g., update UI or show success message
                console.log('Unfollowed user successfully');
                setFollowingUsers(prevState => prevState.filter(id => id !== userId));
            } else {
                // Handle failure, e.g., show error message
                console.error('Failed to unfollow user');
                alert('Failed to unfollow user');
            }
        } catch (error) {
            console.error('Error unfollowing user:', error);
            alert('Error unfollowing user. Please try again.');
        }
    }


    return (
        <div className="container mx-auto mt-8">
            <h1 className="text-3xl font-bold mb-4">Users Page</h1>
            <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {users.map(user => {
                    console.log("followingUsers:", followingUsers);
                    console.log(followingUsers.includes(user.id));
                    return ((
                        <li key={user.id} className="bg-white shadow-black shadow-sm rounded-lg p-4">
                            <div className="flex items-center mb-2">
                                <div className="w-12 h-12 rounded-full overflow-hidden">
                                    <img className="w-full h-full object-cover" src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg" alt="Profile" />
                                </div>
                                <div className="ml-4">
                                    <p className="font-bold">
                                        {user.id === currentUserId ? `${user.username} ( you )` : user.username}
                                    </p>
                                    <p className="text-sm text-gray-600">{user.email}</p>
                                    <p className="text-sm text-gray-600">
                                        Followers: {user.follower_list.length} | Following: {user.following_list.length}
                                    </p>
                                    <p className='text-sm text-gray-600'>Rated: {user.rated_movies.length} movies</p>
                                    <p className='text-sm text-gray-600'>Reviewed: {user.reviewed_movies.length} movies</p>
                                </div>
                            </div>
                            {user.id !== currentUserId && (
                                followingUsers.includes(user.id) ? (
                                    <button
                                        className="block w-auto bg-gray-300 hover:bg-gray-400 text-gray-700 font-bold py-2 px-4 rounded"
                                        onClick={() => handleUnfollow(user.id)}
                                    >
                                        Unfollow
                                    </button>
                                ) : (
                                    <button
                                        className="block w-auto bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
                                        onClick={() => handleFollow(user.id)}
                                    >
                                        Follow
                                    </button>
                                )
                            )}

                        </li>
                    )
                    );
                })}
            </ul>
        </div>
    );
}
