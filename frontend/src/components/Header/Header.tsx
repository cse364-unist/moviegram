import './Header.css';
import { Link} from 'react-router-dom'

function Header({authenticated}) {
    return (
        <header className='header'>
            <div className='header-inner'>
                <nav>
                    <ul>
                        <li><Link to="/">Home</Link></li>
                        <li><Link to="/explore">Explore</Link></li>
                        <li><Link to="/collections">Collections</Link></li>
                        {authenticated ? "Hello, user" : <li><Link to="/login">Login</Link></li>}
                    </ul>
                </nav>
            </div>
        </header>
    );
}

export default Header;
