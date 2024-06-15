import React from 'react';

const MoreCollections: React.FC = () => {
  return (
    <section className="bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        <h2 className="text-2xl font-bold mb-4">Popular Collections</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Your collection cards go here */}
          {/* Example of one collection card */}
          <div className="card">
            <h3>A24 Movies</h3>
            <div className="movies">
              <img src="path/to/movie1.jpg" alt="Movie 1" />
              <img src="path/to/movie2.jpg" alt="Movie 2" />
              <img src="path/to/movie3.jpg" alt="Movie 3" />
              <img src="path/to/movie4.jpg" alt="Movie 4" />
            </div>
            <div className="flex justify-between items-center mt-2">
              <span>1.5k rated</span>
              <button className="bg-black text-white py-1 px-2 rounded">Follow</button>
            </div>
          </div>
          {/* Repeat for other collections */}
        </div>
      </div>
    </section>
  );
};

export default MoreCollections;
