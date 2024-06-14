import './App.css'
import Header from './components/Header/Header'
import { Routes, Route } from 'react-router-dom'
import React, {useEffect, useState} from 'react'; 


//import pages 
import HomePage from './pages/HomePage/HomePage'
import ExplorePage from './pages/ExplorePage/ExplorePage'
import CollectionsPage from './pages/CollectionsPage/CollectionsPage'
import LoginPage from './pages/LoginPage/LoginPage'
import SignUpPage from './pages/SignUpPage/SignUpPage'
import MoviesPage from './pages/MoviesPage/MoviesPage'

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
      <Header authenticated={authenticated}/>
      <div className='flex justify-center bg-white'>
        <Routes>
          <Route path='/*' element={<HomePage />} />
          <Route path="/explore" element={<ExplorePage />} />
          <Route path="/collections" element={<CollectionsPage />} />
          <Route path="/login" element={<LoginPage/>} />
          <Route path="/signup" element={<SignUpPage/>} />
          <Route path="/movies" element={<MoviesPage/>} />
        </Routes>

      </div>

    </>
  )
}

export default App
