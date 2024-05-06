import './Header.css';
import { Link, Routes, Route } from 'react-router-dom'

//import pages 
import HomePage from '../../pages/HomePage';
import ExplorePage from '../../pages/ExplorePage'
import CollectionsPage from '../../pages/CollectionsPage'

function Header() {
    return (
        <header className='header'>
            <div className='header-inner'>
                <nav>
                    <ul>
                        <li><Link to="/">Home</Link></li>
                        <li><Link to="/explore">Explore</Link></li>
                        <li><Link to="/collections">Collections</Link></li>
                    </ul>
                </nav>

                <Routes>
                    <Route path='/*' element={<HomePage />} />
                    <Route path="/explore" element={<ExplorePage />} />
                    <Route path="/collections" element={<CollectionsPage />} />
                </Routes>
            </div>
        </header>
    );
}

export default Header;
