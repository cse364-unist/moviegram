import React from 'react';

interface Movie {
  title: string;
  poster: string;
}

interface CollectionProps {
  title: string;
  movies: Movie[];
}

const Collection: React.FC<CollectionProps> = ({ title, movies }) => {
  const containerBorderRadius = '20px'; // Custom border radius for containers
  const imageBorderRadius = '5px'; // Custom border radius for images

  return (
    <div className="p-4 rounded-lg" style={{ backgroundColor: '#1a1a1a' }}>
      <h3 className="text-xl font-semibold mb-2 text-white">{title}</h3>
      <div className="grid gap-4" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(100px, 1fr))' }}>
        {movies.slice(0, 4).map((movie, index) => (
          <div key={index} className="relative" style={{ borderRadius: containerBorderRadius }}>
            <div style={{ width: '100px', height: '100px', borderRadius: imageBorderRadius }} className="overflow-hidden bg-gray-900">
              <img
                src={movie.poster}
                alt={movie.title}
                className="object-cover w-full h-full"
                style={{ borderRadius: imageBorderRadius }}
              />
            </div>
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center opacity-0 hover:opacity-100 transition-opacity rounded-lg">
              <span className="text-white text-sm">{movie.title}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Collection;
