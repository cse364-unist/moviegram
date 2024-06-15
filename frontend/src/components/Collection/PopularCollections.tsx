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

  const handleMoveLeft = () => {
    setCurrentIndex(prevIndex => Math.max(0, prevIndex - 1));
  };

  const handleMoveRight = () => {
    setCurrentIndex(prevIndex => Math.min(collections.length - 3, prevIndex + 1));
  };

  return (
    <section style={{ backgroundColor: '#EAF0F7', padding: '2rem 0', borderRadius: '20px' }}>
      <div className="container mx-auto px-4">
        <h2 className="text-2xl font-bold mb-4 text-black">Popular Collections</h2>
        <p className="text-sm text-gray-600 mb-4">Here are the most popular movie collections on Moviegram</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {collections.slice(currentIndex, currentIndex + 3).map((collection, index) => (
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
            className={`bg-black text-white py-2 px-3 rounded-md ml-2 ${currentIndex >= collections.length - 3 ? 'opacity-50 cursor-not-allowed' : ''}`}
            disabled={currentIndex >= collections.length - 3}
          >
            <BsChevronRight className="h-5 w-5" /> {/* Right arrow icon */}
          </button>
        </div>
        <button className="mt-4 bg-black text-white py-2 px-4 rounded">Search for more collections</button>
      </div>
    </section>
  );
};

export default PopularCollections;
