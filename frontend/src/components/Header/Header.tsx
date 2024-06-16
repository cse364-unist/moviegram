import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Header.css';

function Header({ authenticated, setAuthenticated }) {
    const navigate = useNavigate();
    const [showDropdown, setShowDropdown] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setShowDropdown(false);
            }
        };

        document.addEventListener('click', handleClickOutside);

        return () => {
            document.removeEventListener('click', handleClickOutside);
        };
    }, []);

    const handleLogout = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:8000/logout/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Token ${token}`,
                },
            });

            if (response.ok) {
                localStorage.removeItem('token');
                setAuthenticated(false);
                navigate('/');
            } else {
                throw new Error('Logout failed');
            }
        } catch (error) {
            console.error('Error during logout:', error);
            alert('Error during logout. Please try again.');
        }
    };

    const toggleDropdown = () => {
        setShowDropdown(!showDropdown);
    };

    const redirectToProfile = () => {
        navigate('/profile');
        setShowDropdown(false); // Close dropdown after navigation
    };

    return (
        <header className='header'>
            <div className='header-inner'>
                <nav>
                    <ul>
                        <li><Link to="/">Home</Link></li>
                        <li><Link to="/explore">Explore</Link></li>
                        <li><Link to="/collections">Collections</Link></li>
                        <li><Link to="/users">Users</Link></li>

                        {authenticated ? (
                            <li className="relative">
                                <div className="avatar cursor-pointer" onClick={toggleDropdown}>
                                    <div className="w-10 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2 overflow-hidden">
                                        <img className="w-full h-full object-cover" src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.jpg" alt="Profile" />
                                    </div>
                                    {showDropdown && (
                                        <div className="dropdown absolute left-11 mt-2 w-24 bg-white rounded-lg shadow-lg py-1">
                                            <button className="block w-full text-left px-4 py-2 text-sm text-gray-800 hover:bg-gray-300" onClick={redirectToProfile}>Profile</button>
                                            <button className="block w-full text-left px-4 py-2 text-sm text-gray-800 hover:bg-gray-300" onClick={handleLogout}>Logout</button>
                                        </div>
                                    )}
                                </div>
                            </li>
                        ) : (
                            <li><Link to="/login">Login</Link></li>
                        )}
                    </ul>
                </nav>
            </div>
        </header>
    );
}

export default Header;
