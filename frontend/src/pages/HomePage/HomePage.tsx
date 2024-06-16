import React, { useEffect, useState } from 'react';
import ReviewActivity from '../../components/ReviewActivity/ReviewActivity';
import RateActivity from '../../components/RateActivity/RateActivity';

interface Activity {
    id: number;
    type: 'review' | 'rate';
    user: string;
    message?: string; // Optional, only for review activities
    rating?: number;  // Optional, only for rate activities
    movie?: string; // Optional, only for review activities
}

const HomePage: React.FC = () => {
    const [activities, setActivities] = useState<Activity[]>([]);

    const token = localStorage.getItem('token'); // Assuming the token is stored in localStorage after login

    useEffect(() => {
        const fetchActivities = async () => {
            try {
                // const response = await fetch('http://localhost:8000/', {
                const response = await fetch('https://mooviegram-4860c7f65aef.herokuapp.com/', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Token ${token}`,
                    },
                });

                if (!response.ok) {
                    throw new Error('Something went wrong');
                }
                const jsonActivities = await response.json();
                setActivities(jsonActivities.activities);
            } catch (error) {
                console.log('Error fetching activities', error);
            }
        };

        if (token) {
            console.log("Token", token);
            fetchActivities();
        } else {
            console.log('No token found, please login');
        }
    }, [token]);

    console.log(">>", activities);

    return (
        <div className="flex flex-col items-center pt-16">
            <div className="text-center mb-6 mt-10">
                <h2 className="text-2xl font-semibold text-gray-600">Friends' activities</h2>
            </div>            <div className="w-full max-w-4xl space-y-4">
                {activities?.map((activity) => {
                    if (activity.type === 'review') {
                        return (
                            <ReviewActivity
                                key={activity.id}
                                message={activity.message!}
                            />
                        );
                    } else if (activity.type === 'rate') {
                        return (
                            <RateActivity
                                key={activity.id}
                                message={activity.message!}
                            />
                        );
                    } else {
                        return null;
                    }
                })}
            </div>
        </div>
    );
};

export default HomePage;
