import React, {useEffect, useState} from 'react'; 
import { Link} from 'react-router-dom'


const LoginInPage = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLoginIn = () => {
        // To do: Implement sign up functionality
    };

    return (
        <div className="flex justify-center items-center h-screen">
            <div className="bg-white shadow-lg border border-gray-200 rounded px-8 pt-6 pb-8 mb-4">
                <h2 className="text-2xl font-bold mb-6">Login</h2>
                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="name">
                        User Name
                    </label>
                    <input
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        id="name"
                        type="text"
                        placeholder="Enter your name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                </div>

                <div className="mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                        Password
                    </label>
                    <input
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                        id="password"
                        type="password"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </div>
                <div className="flex items-center justify-between">
                    <button
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                        type="button"
                        onClick={handleLoginIn}
                    >
                        Login
                    </button>
                </div>
                <p className='mt-4'>Don't have account ? <Link className='text-blue-500' to="/signup">Sign Up</Link></p>
            </div>
        </div>
    );
};

export default LoginInPage;
