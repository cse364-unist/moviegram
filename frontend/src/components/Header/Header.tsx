import './Header.css';
import { Link, useNavigate } from 'react-router-dom';

function Header({ authenticated, setAuthenticated }) {
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            const token = localStorage.getItem('token');
            console.log('Token:', token);
            const response = await fetch('https://mooviegram-4860c7f65aef.herokuapp.com/logout/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                },
            });
            console.log('Logout response:', response);
            if (response.ok){
                localStorage.removeItem('token');
                setAuthenticated(false);
                navigate('/');
            }else{
                throw new Error('Logout failed');
            }
        }catch (error){
            console.log('Error during logout:', error);
            alert('Error during logout');
        }
    };

    return (
        <header className='header'>
            <div className='header-inner'>
                <nav>
                    <ul>
                        <li><Link to="/">Home</Link></li>
                        <li><Link to="/explore">Explore</Link></li>
                        <li><Link to="/collections">Collections</Link></li>
                        {authenticated ? (
                            <li><button onClick={handleLogout}>Logout</button></li>
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
