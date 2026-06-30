import React from 'react';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';

const { FiSquare, FiSmartphone } = FiIcons;

const FormatSelector = ({ format, onUpdate }) => {
  const formats = [
    {
      id: '4:5',
      name: 'Instagram Post',
      ratio: '4:5',
      dimensions: '1080 × 1350',
      icon: FiSquare,
      description: 'Perfect for feed posts'
    },
    {
      id: '9:16',
      name: 'Story / Reel',
      ratio: '9:16',
      dimensions: '1080 × 1920',
      icon: FiSmartphone,
      description: 'Stories and Reels format'
    }
  ];

  return (
    <div className="space-y-3">
      {formats.map((fmt) => (
        <button
          key={fmt.id}
          // Here we use onUpdate which is passed as handleGlobalUpdate from parent
          onClick={() => onUpdate({ format: fmt.id })}
          className={`w-full p-4 text-left border-2 rounded-lg transition-all ${
            format === fmt.id
              ? 'border-purple-500 bg-purple-50'
              : 'border-gray-200 hover:border-gray-300'
          }`}
        >
          <div className="flex items-center space-x-3">
            <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${
              format === fmt.id ? 'bg-purple-100' : 'bg-gray-100'
            }`}>
              <SafeIcon icon={fmt.icon} className={`text-xl ${
                format === fmt.id ? 'text-purple-600' : 'text-gray-600'
              }`} />
            </div>
            <div className="flex-1">
              <h3 className="font-medium text-gray-900">{fmt.name}</h3>
              <p className="text-sm text-gray-600">{fmt.description}</p>
              <p className="text-xs text-gray-500">{fmt.dimensions}</p>
              {format === fmt.id && (
                <span className="mt-1 inline-block text-[10px] font-bold text-purple-600 bg-purple-100 px-2 py-0.5 rounded">
                    ACTIVE
                </span>
              )}
            </div>
          </div>
        </button>
      ))}
    </div>
  );
};

export default FormatSelector;