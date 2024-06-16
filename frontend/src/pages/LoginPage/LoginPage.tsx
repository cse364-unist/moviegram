import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

interface LoginInPageProps {
    setAuthenticated: React.Dispatch<React.SetStateAction<boolean>>;
}

const LoginInPage: React.FC<LoginInPageProps> = ({ setAuthenticated }) => {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const navigate = useNavigate();

    const handleLogin = async (username: string, password: string) => {
        try {
            const response = await fetch('https://mooviegram-4860c7f65aef.herokuapp.com/login/', {
            // const response = await fetch('http://localhost:8000/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) {
                throw new Error('Something went wrong');
            }

            const data = await response.json();
            console.log('Login successful, token:', data.token);

            localStorage.setItem('token', data.token);
            localStorage.setItem('user_id', data.user_id.toString());
            navigate('/');
            setAuthenticated(true);
        } catch (error) {
            console.log('Error during login:', error);
            alert('Invalid credentials or already logged in.');
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await handleLogin(username, password);
    };

    return (
        <div className="flex justify-center items-center h-screen">
            <div className="bg-white shadow-lg border border-gray-200 rounded px-8 pt-6 pb-8 mb-4">
                <h2 className="text-2xl font-bold mb-6">Login</h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-4">
                        <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="name">
                            User Name
                        </label>
                        <input
                            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            id="name"
                            type="text"
                            placeholder="Enter your name"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
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
                            type="submit"
                        >
                            Login
                        </button>
                    </div>
                </form>
                <p className="mt-4">
                    Don't have an account? <Link className="text-blue-500" to="/signup">Sign Up</Link>
                </p>
            </div>
        </div>
    );
};

export default LoginInPage;
