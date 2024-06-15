import React, { useState } from 'react';
import Collection from './Collection';
import CreateCollectionForm from './CreateCollectionForm';
import { BsChevronLeft, BsChevronRight } from 'react-icons/bs';

interface Movie {
  title: string;
  poster: string;
}

interface CollectionProps {
  title: string;
  movies: Movie[];
}

interface CollectionsListProps {
  collections: CollectionProps[];
}

const CollectionsList: React.FC<CollectionsListProps> = ({ collections }) => {
  const [isCreating, setIsCreating] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0); // State to track current collection index
  const [expandedCollection, setExpandedCollection] = useState<CollectionProps | null>(null); // State to track expanded collection

  const handleCreateClick = () => {
    setIsCreating(true);
  };

  const handleCloseForm = () => {
    setIsCreating(false);
  };

  const handleMoveLeft = () => {
    setCurrentIndex(prevIndex => Math.max(0, prevIndex - 1));
  };

  const handleMoveRight = () => {
    setCurrentIndex(prevIndex => Math.min(collections.length - 3, prevIndex + 1));
  };

  const toggleExpand = (collection: CollectionProps) => {
    if (expandedCollection && expandedCollection.title === collection.title) {
      setExpandedCollection(null); // Close expanded view if same collection is clicked
    } else {
      setExpandedCollection(collection);
    }
  };

  return (
    <section style={{ backgroundColor: '#EAF0F7', padding: '2rem 0', borderRadius: '20px', marginTop: '5rem' }}>
      <div className="container mx-auto px-4 relative">
        <h2 className="text-2xl font-bold mb-4 text-black">Your Movie collections</h2>
        <p className="text-sm text-gray-600 mb-4">Collections you created or saved recently</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {collections.slice(currentIndex, currentIndex + 3).map((collection, index) => (
            <div key={index} className="mb-6" onClick={() => toggleExpand(collection)}>
              <Collection title={collection.title} movies={collection.movies} onClick={() => {}} />
            </div>
          ))}
          {isCreating && (
            <div className="col-span-1 md:col-span-2 lg:col-span-3">
              <CreateCollectionForm onClose={handleCloseForm} />
            </div>
          )}
        </div>
        {!isCreating && (
          <div className="flex justify-between">
            <button
              onClick={handleMoveLeft}
              className={`bg-black text-white py-2 px-3 rounded-md mr-2 ${currentIndex === 0 ? 'opacity-50 cursor-not-allowed' : ''}`}
              disabled={currentIndex === 0}
              style={{ marginBottom: '10px' }} // Adjust margin-bottom here
            >
              <BsChevronLeft className="h-5 w-5" /> {/* Left arrow icon */}
            </button>
            <button
              onClick={handleMoveRight}
              className={`bg-black text-white py-2 px-3 rounded-md ml-2 ${currentIndex >= collections.length - 3 ? 'opacity-50 cursor-not-allowed' : ''}`}
              disabled={currentIndex >= collections.length - 3}
              style={{ marginBottom: '10px' }} // Adjust margin-bottom here
            >
              <BsChevronRight className="h-5 w-5" /> {/* Right arrow icon */}
            </button>
          </div>
        )}
      </div>
      {!isCreating && (
        <div className="flex justify-center mt-4">
          <button
            onClick={handleCreateClick}
            className="bg-black text-white py-2 px-4 rounded"
          >
            Create a new collection
          </button>
        </div>
      )}
      {expandedCollection && (
        <div className="fixed inset-0 bg-white z-50 overflow-y-auto pt-20">
          <div className="container mx-auto px-4 py-8">
            <h2 className="text-2xl font-bold mb-4 text-black">{expandedCollection.title}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
              {expandedCollection.movies.map((movie, index) => (
                <div key={index} className="relative">
                  <div className="overflow-hidden bg-gray-900">
                    <img
                      src={movie.poster}
                      alt={movie.title}
                      className="object-cover w-full h-full"
                    />
                  </div>
                  <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity">
                    <span className="text-white text-sm">{movie.title}</span>
                  </div>
                </div>
              ))}
            </div>
            <button onClick={() => setExpandedCollection(null)} className="mt-4 bg-black text-white py-2 px-4 rounded">
              Close
            </button>
          </div>
        </div>
      )}
    </section>
  );
};

export default CollectionsList;
