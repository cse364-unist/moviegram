import React, { useState } from 'react';
import Collection from './Collection';
import { BsChevronLeft, BsChevronRight } from 'react-icons/bs'; // Import arrow icons

interface Movie {
  title: string;
  poster: string;
}

interface CollectionProps {
  title: string;
  movies: Movie[];
}

interface PopularCollectionsProps {
  collections: CollectionProps[];
}

const PopularCollections: React.FC<PopularCollectionsProps> = ({ collections }) => {
  const [currentIndex, setCurrentIndex] = useState(0); // State to track current collection index
  const [expanded, setExpanded] = useState(false); // State to track expanded view
  const [searchTerm, setSearchTerm] = useState(''); // State to track search term

  const handleMoveLeft = () => {
    setCurrentIndex(prevIndex => Math.max(0, prevIndex - 3));
  };

  const handleMoveRight = () => {
    setCurrentIndex(prevIndex => Math.min(collections.length - 3, prevIndex + 3));
  };

  const toggleExpand = () => {
    setExpanded(!expanded);
  };

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const filteredCollections = collections.filter(collection =>
    collection.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <section style={{ backgroundColor: '#EAF0F7', padding: '2rem 0', borderRadius: '20px', marginTop: '5rem' }}>
      <div className="container mx-auto px-4">
        <h2 className="text-2xl font-bold mb-4 text-black">Popular Collections</h2>
        <p className="text-sm text-gray-600 mb-4">Here are the most popular movie collections on Moviegram</p>
        {!expanded && (
          <div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredCollections.slice(currentIndex, currentIndex + 3).map((collection, index) => (
                <Collection key={index} title={collection.title} movies={collection.movies} />
              ))}
            </div>
            <div className="flex justify-between mt-4">
              <button
                onClick={handleMoveLeft}
                className={`bg-black text-white py-2 px-3 rounded-md mr-2 ${currentIndex === 0 ? 'opacity-50 cursor-not-allowed' : ''}`}
                disabled={currentIndex === 0}
              >
                <BsChevronLeft className="h-5 w-5" /> {/* Left arrow icon */}
              </button>
              <button
                onClick={handleMoveRight}
                className={`bg-black text-white py-2 px-3 rounded-md ml-2 ${currentIndex >= filteredCollections.length - 3 ? 'opacity-50 cursor-not-allowed' : ''}`}
                disabled={currentIndex >= filteredCollections.length - 3}
              >
                <BsChevronRight className="h-5 w-5" /> {/* Right arrow icon */}
              </button>
            </div>
            <button
              onClick={toggleExpand}
              className="mt-4 bg-black text-white py-2 px-4 rounded"
            >
              Search for more collections
            </button>
          </div>
        )}
        {expanded && (
          <div className="fixed inset-0 bg-white z-50 overflow-y-auto pt-20"> {/* Adjust pt-20 to add padding-top */}
            <div className="container mx-auto px-4 py-8">
              <h2 className="text-2xl font-bold mb-4 text-black">Popular Collections</h2>
              <p className="text-sm text-gray-600 mb-4">Here are the most popular movie collections on Moviegram</p>
              <input
                type="text"
                placeholder="Search in for collections..."
                value={searchTerm}
                onChange={handleSearchChange}
                className="border border-gray-300 rounded py-2 px-4 mb-4 focus:outline-none focus:border-blue-500"
              />
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
                {filteredCollections.map((collection, index) => (
                  <Collection key={index} title={collection.title} movies={collection.movies} />
                ))}
              </div>
              <button onClick={toggleExpand} className="mt-4 bg-black text-white py-2 px-4 rounded">
                Go Back
              </button>
            </div>
          </div>
        )}
      </div>
    </section>
  );
};

export default PopularCollections;
