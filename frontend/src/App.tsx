import './App.css'
import Header from './components/Header/Header'
import { Routes, Route } from 'react-router-dom'
import {useEffect, useState} from 'react'; 


//import pages 
import HomePage from './pages/HomePage/HomePage'
import ExplorePage from './pages/ExplorePage/ExplorePage'
import CollectionsPage from './pages/CollectionsPage/CollectionsPage'
import LoginPage from './pages/LoginPage/LoginPage'
import SignUpPage from './pages/SignUpPage/SignUpPage'
import MoviesPage from './pages/MoviesPage/MoviesPage'
import UsersPage from './pages/UsersPage/UsersPage'
import ProfilePage from './pages/ProfilePage/ProfilePage';

function App() {
  const [authenticated, setAuthenticated] = useState(false) 

  useEffect(() => {
    const token = localStorage.getItem('token') 
    if(token){
      setAuthenticated(true) 
    }
  }, [])


  return (
    <>
      <Header authenticated={authenticated} setAuthenticated={setAuthenticated}/>
      <div className='flex justify-center bg-white'>
        <Routes>
          <Route path='/*' element={<HomePage />} />
          <Route path="/explore" element={<ExplorePage />} />
          <Route path="/collections" element={<CollectionsPage />} />
          <Route path="/login" element={<LoginPage setAuthenticated={setAuthenticated}/>} />
          <Route path="/signup" element={<SignUpPage/>} />
          <Route path="/movies" element={<MoviesPage/>} />
          <Route path="/users" element={<UsersPage/>}/>
          <Route path="/profile" element={<ProfilePage/>}/>
        </Routes>

      </div>

    </>
  )
}

export default App
