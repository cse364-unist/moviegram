import React, { useState } from 'react';

interface CreateCollectionFormProps {
  onClose: () => void;
}

const CreateCollectionForm: React.FC<CreateCollectionFormProps> = ({ onClose }) => {
  const [visibility, setVisibility] = useState<string>('private'); // State to track visibility option

  const handleVisibilityChange = (option: string) => {
    setVisibility(option);
  };

  return (
    <div className="bg-white p-8 rounded shadow-md max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-4 text-black">Create a Collection</h2>
      <form>
        <div className="mb-4">
          <label className="block text-gray-700">Name Of Collection</label>
          <input
            type="text"
            className="w-full px-3 py-2 border border-purple-500 rounded text-black bg-transparent"
            defaultValue="Fav_action movies"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Describe Your Collection</label>
          <textarea
            className="w-full px-3 py-2 border border-purple-500 rounded text-black bg-transparent"
            rows={4}
            defaultValue="A collection of my favorite action movies!"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700">Add Movies To Your Collection</label>
          <div className="w-full px-3 py-2 border border-purple-500 rounded flex justify-center items-center">
            <img src="path/to/black_panther.jpg" alt="Black Panther" className="w-24 h-36 rounded"/>
          </div>
        </div>
        <div className="mb-4 flex items-center">
          <label className="inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={visibility === 'private'}
              onChange={() => handleVisibilityChange('private')}
              className={`form-checkbox h-5 w-5 text-purple-500 border-2 ${visibility === 'private' ? 'bg-purple-500 border-purple-500' : 'bg-transparent border-purple-500'} rounded focus:ring-purple-400`}
            />
            <span className={`ml-2 ${visibility === 'public' ? 'text-gray-700' : 'text-black'}`}>Private</span>
          </label>
          <label className="inline-flex items-center ml-4 cursor-pointer">
            <input
              type="checkbox"
              checked={visibility === 'public'}
              onChange={() => handleVisibilityChange('public')}
              className={`form-checkbox h-5 w-5 text-purple-500 border-2 ${visibility === 'public' ? 'bg-purple-500 border-purple-500' : 'bg-transparent border-purple-500'} rounded focus:ring-purple-400`}
            />
            <span className={`ml-2 ${visibility === 'private' ? 'text-gray-700' : 'text-black'}`}>Public</span>
          </label>
        </div>
        <div className="flex justify-end">
          <button type="button" className="bg-black text-white py-2 px-4 rounded">Save</button>
          <button type="button" onClick={onClose} className="ml-4 bg-gray-500 text-white py-2 px-4 rounded">Cancel</button>
        </div>
      </form>
    </div>
  );
};

export default CreateCollectionForm;
