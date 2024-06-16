import React from 'react';
import { FaUser } from 'react-icons/fa'; // Assuming react-icons is installed

interface RateActivityProps {
    message: string;
}
const RateActivity: React.FC<RateActivityProps> = ({ message}) => {
    return (
        <div className="p-6 mb-6 border rounded-lg shadow-lg bg-white">
            <div className="flex items-center mb-4">
                <FaUser className="text-blue-500 mr-2" />
            </div>
            <p className="mt-4 text-gray-700">{message}</p>
        </div>
    );
};

export default RateActivity;
