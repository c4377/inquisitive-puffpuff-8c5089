import React, { useState } from 'react';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';

const { FiUpload, FiImage } = FiIcons;

const ImageUpload = ({ onImageSelect }) => {
  const [dragOver, setDragOver] = useState(false);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        onImageSelect(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragOver(false);
    const file = event.dataTransfer.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        onImageSelect(e.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          <SafeIcon icon={FiUpload} className="inline mr-2" /> Upload Image
        </label>
        <div 
          className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${dragOver ? 'border-purple-400 bg-purple-50' : 'border-gray-300'}`}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
        >
          <SafeIcon icon={FiImage} className="text-4xl text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 mb-2">Drag & drop an image here, or click to select</p>
          <input type="file" accept="image/*" onChange={handleFileUpload} className="hidden" id="image-upload" />
          <label htmlFor="image-upload" className="inline-block bg-purple-600 text-white px-4 py-2 rounded-lg cursor-pointer hover:bg-purple-700 transition-colors">
            Choose File
          </label>
        </div>
      </div>
      
      {/* Stock Images Removed */}
      <div className="p-4 bg-gray-50 rounded-lg text-xs text-gray-500 text-center">
         Nutze den "Magic Gen" Tab im Editor, um Hintergründe zu generieren.
      </div>
    </div>
  );
};

export default ImageUpload;