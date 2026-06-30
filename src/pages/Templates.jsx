import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';

const { FiGrid, FiImage, FiVideo, FiStar, FiFilter, FiSearch, FiArrowRight } = FiIcons;

const Templates = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const categories = [
    { id: 'all', label: 'All Templates', icon: FiGrid },
    { id: 'carousel', label: 'Carousels', icon: FiImage },
    { id: 'story', label: 'Stories', icon: FiVideo },
    { id: 'single', label: 'Posts', icon: FiStar }
  ];

  // 10 HIGH QUALITY TEMPLATES
  const templates = [
    {
      id: 1,
      name: 'The Viral Hook',
      category: 'carousel',
      format: '4:5',
      layout: 'centered_focus',
      preview: 'https://images.unsplash.com/photo-1616469829941-c7200edec809?w=400&h=500&fit=crop',
      style: 'Bold & Impactful',
      description: 'Perfect for starting a carousel with a strong statement.'
    },
    {
      id: 2,
      name: 'Expert Quote',
      category: 'single',
      format: '4:5',
      layout: 'minimal_quote',
      preview: 'https://images.unsplash.com/photo-1493612276216-ee3925520721?w=400&h=500&fit=crop',
      style: 'Minimal Editorial',
      description: 'Clean typography to showcase authority and wisdom.'
    },
    {
      id: 3,
      name: 'Daily Reminder',
      category: 'story',
      format: '9:16',
      layout: 'editorial_mask',
      preview: 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&h=711&fit=crop',
      style: 'Soft Aesthetic',
      description: 'Gentle morning reminder for your community.'
    },
    {
      id: 4,
      name: 'Strategic Checklist',
      category: 'carousel',
      format: '4:5',
      layout: 'aesthetic_checklist',
      preview: 'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=400&h=500&fit=crop',
      style: 'Functional & Dark',
      description: 'High-value educational content in list format.'
    },
    {
      id: 5,
      name: 'The Split View',
      category: 'single',
      format: '4:5',
      layout: 'split_vertical_editorial',
      preview: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&h=500&fit=crop',
      style: 'Modern Editorial',
      description: 'Balance image and text perfectly.'
    },
    {
      id: 6,
      name: 'Event Countdown',
      category: 'story',
      format: '9:16',
      layout: 'diagonal_overlay',
      preview: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400&h=711&fit=crop',
      style: 'High Energy',
      description: 'Build hype for launches or events.'
    },
    {
      id: 7,
      name: 'Myth vs. Fact',
      category: 'single',
      format: '4:5',
      layout: 'centered_focus',
      preview: 'https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=400&h=500&fit=crop',
      style: 'Educational',
      description: 'Bust myths in your niche effectively.'
    },
    {
      id: 8,
      name: 'Behind The Scenes',
      category: 'story',
      format: '9:16',
      layout: 'centered_focus',
      preview: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=400&h=711&fit=crop',
      style: 'Authentic',
      description: 'Show the reality behind the polished feed.'
    },
    {
      id: 9,
      name: 'Product Teaser',
      category: 'single',
      format: '4:5',
      layout: 'editorial_mask',
      preview: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=500&fit=crop',
      style: 'Clean Focus',
      description: 'Highlight a specific product or offer.'
    },
    {
      id: 10,
      name: 'Weekly Recap',
      category: 'carousel',
      format: '4:5',
      layout: 'diagonal_overlay',
      preview: 'https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=400&h=500&fit=crop',
      style: 'Structured',
      description: 'Summarize the wins of the week.'
    }
  ];

  const filteredTemplates = templates.filter(template => {
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
    const matchesSearch = template.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          template.style.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-32">
      {/* Header */}
      <motion.div 
        className="text-center mb-10"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
          Premium Templates
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Professionell gestaltete Templates im sinn_brands-Stil. 
          Wähle eine Vorlage, um direkt im Editor zu starten.
        </p>
      </motion.div>

      {/* Filters */}
      <motion.div 
        className="flex flex-col sm:flex-row gap-4 mb-10"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
      >
        {/* Search */}
        <div className="relative flex-1">
          <SafeIcon icon={FiSearch} className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input 
            type="text" 
            placeholder="Search templates..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-shadow shadow-sm"
          />
        </div>

        {/* Categories */}
        <div className="flex space-x-2 overflow-x-auto pb-2 sm:pb-0 no-scrollbar">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`flex items-center space-x-2 px-5 py-3 rounded-xl font-bold text-sm whitespace-nowrap transition-all duration-200 ${
                selectedCategory === category.id 
                  ? 'bg-purple-600 text-white shadow-lg transform scale-105' 
                  : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200'
              }`}
            >
              <SafeIcon icon={category.icon} />
              <span>{category.label}</span>
            </button>
          ))}
        </div>
      </motion.div>

      {/* Templates Grid */}
      <motion.div 
        className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.4 }}
      >
        {filteredTemplates.map((template, index) => (
          <motion.div
            key={template.id}
            className="group bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 border border-gray-100"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            {/* Preview Image Container */}
            <div className="relative overflow-hidden bg-gray-100 aspect-[4/5] cursor-pointer">
              <img 
                src={template.preview} 
                alt={template.name} 
                className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
              />
              
              {/* Overlay on Hover */}
              <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-all duration-300 flex items-center justify-center backdrop-blur-[2px]">
                <Link 
                  to={`/create?layout=${template.layout}&format=${template.format === '9:16' ? 'story' : '4:5'}`}
                  className="bg-white text-gray-900 px-6 py-3 rounded-xl font-bold text-sm transform translate-y-4 group-hover:translate-y-0 transition-all duration-300 shadow-xl flex items-center hover:bg-purple-50"
                >
                  Template nutzen <SafeIcon icon={FiArrowRight} className="ml-2" />
                </Link>
              </div>

              {/* Badge */}
              <div className="absolute top-3 right-3">
                <span className="bg-white/95 backdrop-blur text-[10px] font-bold px-2.5 py-1 rounded-md shadow-sm uppercase tracking-wide text-gray-800">
                  {template.format}
                </span>
              </div>
            </div>

            {/* Content */}
            <div className="p-5">
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-bold text-gray-900 group-hover:text-purple-600 transition-colors">
                  {template.name}
                </h3>
                <span className="text-[10px] font-bold text-purple-600 bg-purple-50 px-2 py-1 rounded uppercase tracking-wider">
                  {template.category}
                </span>
              </div>
              <p className="text-sm text-gray-500 line-clamp-2 leading-relaxed">
                {template.description}
              </p>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* Empty State */}
      {filteredTemplates.length === 0 && (
        <motion.div 
          className="text-center py-24 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <SafeIcon icon={FiFilter} className="text-5xl text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-gray-900 mb-2">Keine Templates gefunden</h3>
          <p className="text-gray-500">Versuche es mit einem anderen Suchbegriff oder Kategorie.</p>
          <button 
             onClick={() => {setSelectedCategory('all'); setSearchTerm('');}}
             className="mt-4 text-purple-600 font-bold text-sm hover:underline"
          >
            Alle anzeigen
          </button>
        </motion.div>
      )}
    </div>
  );
};

export default Templates;