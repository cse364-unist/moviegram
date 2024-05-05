import './Header.css';

function Header() {
    return (
        <header className='header'>
            <div className='header-inner'>
                {/* <img className='logo' src={'images/Logo.svg'} alt='' /> */}

                <nav>
                    <ul>
                        <li><a href=''>Home</a></li>
                        <li><a href=''>Explore</a></li>
                        <li><a href=''>Collections</a></li>
                    </ul>
                </nav>
                {/*                    
                    <div className='login'>
                    </div> */}
            </div>
        </header>
    )
}

export default Header; 