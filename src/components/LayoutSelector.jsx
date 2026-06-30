import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FiLayout, FiGrid, FiLayers, FiType, FiImage, FiArrowRight, FiList, FiMessageSquare, FiTwitter, FiBox, FiSquare } from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { useBrand } from '../context/BrandContext';
import { brandRuleSets } from '../constants/brandData';

const LayoutSelector = () => {
  const { brand } = useBrand();

  // Expanded Categories with new Smart Layouts
  const categories = [
    { id: 'editorial', name: 'Editorial & Story', icon: FiType, layouts: ['editorial_classic', 'minimal', 'bold_statement'] },
    { id: 'visual', name: 'High Impact', icon: FiImage, layouts: ['paper_box', 'split_color', 'photo_frame'] },
    { id: 'social', name: 'Social Native', icon: FiMessageSquare, layouts: ['tweet_card', 'notification', 'chat_bubble'] },
  ];

  return (
    <div className="h-full overflow-y-auto p-4 bg-gray-50/50">
      <div className="mb-6">
        <h2 className="text-lg font-bold text-gray-800 mb-1">Layout Library</h2>
        <p className="text-xs text-gray-500">Select a style for your current slide</p>
      </div>

      <div className="space-y-8">
        {categories.map((cat) => (
          <div key={cat.id}>
            <div className="flex items-center gap-2 mb-3 text-gray-400 uppercase tracking-wider text-xs font-semibold">
              <SafeIcon icon={cat.icon} />
              {cat.name}
            </div>
            <div className="grid grid-cols-2 gap-3">
              {cat.layouts.map((layoutId) => (
                <div 
                  key={layoutId} 
                  className="group relative aspect-video bg-white rounded-lg border border-gray-200 hover:border-purple-500 hover:shadow-md transition-all cursor-pointer overflow-hidden"
                >
                  {/* Preview Placeholder */}
                  <div className="absolute inset-0 p-3 flex flex-col justify-center items-center bg-gray-50">
                    <div className="w-3/4 h-2 bg-gray-200 rounded mb-2"></div>
                    <div className="w-1/2 h-2 bg-gray-200 rounded"></div>
                    {layoutId === 'split_color' && <div className="absolute bottom-0 left-0 right-0 h-1/2 bg-purple-100 opacity-50"></div>}
                    {layoutId === 'paper_box' && <div className="absolute inset-4 bg-white shadow-sm border border-gray-100"></div>}
                  </div>
                  
                  <div className="absolute bottom-0 left-0 right-0 p-2 bg-white/90 backdrop-blur-sm border-t border-gray-100 text-xs font-medium text-gray-700">
                    {layoutId.replace('_', ' ')}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LayoutSelector;