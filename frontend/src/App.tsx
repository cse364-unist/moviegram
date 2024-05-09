import './App.css'
import Header from './components/Header/Header'
import { Routes, Route } from 'react-router-dom'

//import pages 
import HomePage from './pages/HomePage/HomePage'
import ExplorePage from './pages/ExplorePage/ExplorePage'
import CollectionsPage from './pages/CollectionsPage/CollectionsPage'

function App() {
  return (
    <>
      <Header />
      <div className='main'>
        <Routes>
          <Route path='/*' element={<HomePage />} />
          <Route path="/explore" element={<ExplorePage />} />
          <Route path="/collections" element={<CollectionsPage />} />
        </Routes>

      </div>

    </>
  )
}

export default App
