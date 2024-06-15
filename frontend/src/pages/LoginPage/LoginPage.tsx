import React, {useEffect, useState} from 'react'; 
import { Link, useNavigate} from 'react-router-dom'


const LoginInPage = ({setAuthenticated}) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (username, password) => {
        try {
            const response = await fetch('https://mooviegram-4860c7f65aef.herokuapp.com/login/', {
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
            navigate('/movies');
            setAuthenticated(true);

        } catch (error) {
            console.log('Error during login:', error);
            alert('Invalid credentials or already logged in.');

        }
    }; 
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        await handleLogin(username, password);
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
                        type="button"
                        onClick={handleSubmit}
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
