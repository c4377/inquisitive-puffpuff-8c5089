import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import Canvas from '../components/Canvas';
import StyleShifter from '../components/StyleShifter'; // IMPORT
import { useBrand } from '../context/BrandContext';
import { Link } from 'react-router-dom';

const { FiGrid, FiPlus, FiEdit3, FiImage, FiTrash2, FiCamera, FiX, FiCheck, FiList, FiUpload, FiMenu, FiHeart, FiMessageCircle, FiSend, FiUser, FiChevronDown, FiLayers, FiRefreshCw } = FiIcons;

const FeedPreview = () => {
  const { brandSettings, updateFeedProfile, addPostToFeed, removePostFromFeed } = useBrand();
  const feedProfile = brandSettings.feedProfile || {};
  const contentPlan = brandSettings.contentPlan || [];
  const savedDesigns = brandSettings.savedDesigns || [];
  
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  const [showLibrary, setShowLibrary] = useState(false);
  const [showShifter, setShowShifter] = useState(false); // SHIFTER STATE
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'
  const [tempProfile, setTempProfile] = useState({ ...feedProfile });

  // Handle Profile Pic Upload
  const handleProfileImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        alert("Das Bild ist zu groß (Max 5MB).");
        return;
      }
      const reader = new FileReader();
      reader.onload = (ev) => {
        updateFeedProfile({ profileImage: ev.target.result });
      };
      reader.readAsDataURL(file);
    }
  };

  // Handle Highlight Upload
  const handleHighlightUpload = (id, e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (ev) => {
        const newHighlights = feedProfile.highlights.map(h => 
          h.id === id ? { ...h, image: ev.target.result } : h
        );
        updateFeedProfile({ highlights: newHighlights });
      };
      reader.readAsDataURL(file);
    }
  };

  // Quick Post Upload
  const handleQuickPostUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (ev) => {
        const newPost = {
          id: Date.now(),
          background: ev.target.result,
          type: 'photo',
          layout: 'centered_focus',
          text: '',
          overlay: 0,
          imageScale: 1,
          isExtra: true
        };
        addPostToFeed(newPost);
      };
      reader.readAsDataURL(file);
    }
  };

  const addHighlight = () => {
    const newId = Date.now();
    updateFeedProfile({
      highlights: [...(feedProfile.highlights || []), { id: newId, title: 'Neu', image: null }]
    });
  };

  const deleteHighlight = (id) => {
    if (window.confirm("Highlight löschen?")) {
      updateFeedProfile({
        highlights: feedProfile.highlights.filter(h => h.id !== id)
      });
    }
  };

  const updateHighlightTitle = (id, newTitle) => {
    updateFeedProfile({
      highlights: feedProfile.highlights.map(h => h.id === id ? { ...h, title: newTitle } : h)
    });
  };

  const saveProfileChanges = () => {
    updateFeedProfile(tempProfile);
    setIsEditingProfile(false);
  };

  // Combine Content Plan + Extra Posts
  const planPosts = contentPlan.map(day => {
    const slide = day.slides[0];
    return { ...slide, uniqueId: `plan-${day.day}`, isPlan: true, dayTitle: day.title };
  });
  
  const extraPosts = (feedProfile.extraPosts || []).map(post => ({ ...post, uniqueId: `extra-${post.id}`, isExtra: true }));
  
  const allPosts = [...extraPosts, ...planPosts];
  const brandConfig = brandSettings.currentBrandConfig;

  return (
    <div className="max-w-md mx-auto bg-white min-h-screen shadow-2xl border-x border-gray-100 pb-20 overflow-hidden relative">
      
      {/* INSTAGRAM HEADER */}
      <div className="relative z-10 bg-white border-b border-gray-100 px-4 py-3 flex items-center justify-between">
        <div className="font-bold text-lg flex items-center">
          {feedProfile.username} <SafeIcon icon={FiChevronDown} className="ml-1 text-xs" />
        </div>
        <div className="flex space-x-4 text-2xl items-center">
           {/* SHIFTER TOGGLE */}
           <button 
             onClick={() => setShowShifter(!showShifter)}
             className={`text-lg transition-colors ${showShifter ? 'text-purple-600' : 'text-gray-400 hover:text-gray-900'}`}
             title="Style Shifter"
           >
             <SafeIcon icon={FiRefreshCw} />
           </button>

          <label className="cursor-pointer hover:text-purple-600 transition-colors" title="Foto direkt hochladen">
            <SafeIcon icon={FiPlus} />
            <input type="file" accept="image/*" onChange={handleQuickPostUpload} className="hidden" />
          </label>
          <button title="Menu"><SafeIcon icon={FiMenu} /></button>
        </div>
      </div>

      {/* SHIFTER PANEL (Collapsible) */}
      <AnimatePresence>
        {showShifter && (
            <motion.div 
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="overflow-hidden bg-gray-50 border-b border-gray-200"
            >
                <div className="p-4">
                    <StyleShifter compact={true} />
                    <p className="text-[10px] text-gray-400 mt-2 text-center">
                        Änderungen wirken sich live auf die Vorschau aus (Override Mode).
                    </p>
                </div>
            </motion.div>
        )}
      </AnimatePresence>

      {/* PROFILE INFO */}
      <div className="px-4 py-4 relative z-0">
        <div className="flex items-center justify-between mb-4">
          {/* Profile Pic */}
          <div className="relative flex-shrink-0">
            <div className="w-20 h-20 rounded-full p-[2px] bg-gradient-to-tr from-yellow-400 via-red-500 to-purple-600">
              <div className="w-full h-full rounded-full border-2 border-white overflow-hidden bg-gray-100 flex items-center justify-center relative bg-white">
                {feedProfile.profileImage ? (
                  <img src={feedProfile.profileImage} alt="Profile" className="w-full h-full object-cover" />
                ) : (
                  <SafeIcon icon={FiImage} className="text-gray-300 text-2xl" />
                )}
              </div>
            </div>
            <label className="absolute bottom-0 right-0 bg-blue-500 text-white p-1.5 rounded-full border-2 border-white cursor-pointer shadow-md active:scale-95 transition-transform z-10 flex items-center justify-center">
              <SafeIcon icon={FiPlus} className="text-xs font-bold" />
              <input type="file" accept="image/*" onChange={handleProfileImageUpload} className="hidden" />
            </label>
          </div>
          
          {/* Stats */}
          <div className="flex flex-1 justify-around text-center ml-4">
            <div>
              <div className="font-bold text-lg">{allPosts.length}</div>
              <div className="text-xs text-gray-500">Beiträge</div>
            </div>
            <div>
              <div className="font-bold text-lg">{feedProfile.stats?.followers || 0}</div>
              <div className="text-xs text-gray-500">Follower</div>
            </div>
            <div>
              <div className="font-bold text-lg">{feedProfile.stats?.following || 0}</div>
              <div className="text-xs text-gray-500">Gefolgt</div>
            </div>
          </div>
        </div>

        {/* Bio */}
        <div className="text-sm mb-4">
          {isEditingProfile ? (
            <div className="space-y-2 bg-gray-50 p-3 rounded-lg border border-gray-200 shadow-sm animate-fade-in">
                {/* ... Edit Form (Same as before) ... */}
                <div className="flex justify-between items-center mb-2">
                    <span className="text-xs font-bold uppercase text-gray-400">Profil bearbeiten</span>
                    <label className="text-xs text-blue-600 font-bold cursor-pointer flex items-center">
                        <SafeIcon icon={FiUpload} className="mr-1" /> Bild ändern
                        <input type="file" accept="image/*" onChange={handleProfileImageUpload} className="hidden" />
                    </label>
                </div>
                <input value={tempProfile.name} onChange={(e) => setTempProfile({...tempProfile, name: e.target.value})} className="w-full font-bold bg-white border border-gray-200 rounded px-2 py-1 focus:outline-none focus:border-blue-500" placeholder="Name" />
                <textarea value={tempProfile.bio} onChange={(e) => setTempProfile({...tempProfile, bio: e.target.value})} className="w-full bg-white border border-gray-200 rounded px-2 py-1 focus:outline-none focus:border-blue-500 text-xs" rows={3} placeholder="Bio" />
                <input value={tempProfile.website} onChange={(e) => setTempProfile({...tempProfile, website: e.target.value})} className="w-full text-blue-900 bg-white border border-gray-200 rounded px-2 py-1 focus:outline-none focus:border-blue-500" placeholder="Website" />
                <div className="flex justify-end space-x-2 pt-2">
                    <button onClick={() => setIsEditingProfile(false)} className="px-3 py-1 text-red-500 text-xs font-bold border border-red-100 rounded hover:bg-red-50">Abbrechen</button>
                    <button onClick={saveProfileChanges} className="px-3 py-1 bg-blue-500 text-white text-xs font-bold rounded hover:bg-blue-600">Speichern</button>
                </div>
            </div>
          ) : (
            <>
              <div className="font-bold">{feedProfile.name}</div>
              <div className="whitespace-pre-wrap">{feedProfile.bio}</div>
              <div className="text-blue-900 font-medium mt-1">{feedProfile.website}</div>
            </>
          )}
        </div>

        {/* Action Buttons */}
        {!isEditingProfile && (
          <div className="flex space-x-2 text-sm font-bold">
            <button onClick={() => { setTempProfile({...feedProfile}); setIsEditingProfile(true); }} className="flex-1 bg-gray-100 py-1.5 rounded-lg hover:bg-gray-200 transition-colors">
              Profil bearbeiten
            </button>
            <button className="flex-1 bg-gray-100 py-1.5 rounded-lg hover:bg-gray-200 transition-colors">
              Profil teilen
            </button>
          </div>
        )}
      </div>

      {/* HIGHLIGHTS */}
      <div className="px-4 mb-2 overflow-x-auto no-scrollbar relative z-0">
        <div className="flex space-x-4 py-2">
          {feedProfile.highlights?.map(highlight => (
            <div key={highlight.id} className="flex flex-col items-center space-y-1 flex-shrink-0 group relative">
              <div className="w-16 h-16 rounded-full border border-gray-200 p-[2px]">
                <div className="w-full h-full rounded-full bg-gray-100 overflow-hidden flex items-center justify-center relative">
                  {highlight.image ? (
                    <img src={highlight.image} alt={highlight.title} className="w-full h-full object-cover" />
                  ) : (
                    <SafeIcon icon={FiImage} className="text-gray-300" />
                  )}
                  {/* Highlight Edit Overlay */}
                  <label className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 cursor-pointer text-white transition-opacity">
                    <SafeIcon icon={FiCamera} className="text-lg" />
                    <input type="file" accept="image/*" onChange={(e) => handleHighlightUpload(highlight.id, e)} className="hidden" />
                  </label>
                </div>
              </div>
              <input 
                value={highlight.title} 
                onChange={(e) => updateHighlightTitle(highlight.id, e.target.value)}
                className="text-xs text-center w-16 bg-transparent focus:outline-none focus:border-b border-gray-300 truncate"
              />
              <button 
                onClick={() => deleteHighlight(highlight.id)}
                className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full p-0.5 opacity-0 group-hover:opacity-100 transition-opacity shadow-sm z-10"
              >
                <SafeIcon icon={FiX} className="text-[10px]" />
              </button>
            </div>
          ))}
          <button onClick={addHighlight} className="flex flex-col items-center space-y-1 flex-shrink-0">
            <div className="w-16 h-16 rounded-full border border-gray-200 flex items-center justify-center bg-gray-50 hover:bg-gray-100 transition-colors">
              <SafeIcon icon={FiPlus} className="text-2xl text-gray-400" />
            </div>
            <span className="text-xs text-gray-500">Neu</span>
          </button>
        </div>
      </div>

      {/* TABS (Grid vs List) */}
      <div className="flex border-t border-gray-200 mt-2 sticky top-[135px] bg-white z-10 transition-all">
        <button onClick={() => setViewMode('grid')} className={`flex-1 py-2 border-b-2 flex justify-center transition-colors ${viewMode === 'grid' ? 'border-black text-black' : 'border-transparent text-gray-400'}`}>
          <SafeIcon icon={FiGrid} className="text-xl" />
        </button>
        <button onClick={() => setViewMode('list')} className={`flex-1 py-2 border-b-2 flex justify-center transition-colors ${viewMode === 'list' ? 'border-black text-black' : 'border-transparent text-gray-400'}`} title="Timeline View (4:5)">
          <SafeIcon icon={FiList} className="text-xl" />
        </button>
        <button className="flex-1 py-2 flex justify-center text-gray-400 border-b-2 border-transparent">
          <SafeIcon icon={FiUser} className="text-xl" />
        </button>
      </div>

      {/* CONTENT AREA */}
      <div className="pb-20 min-h-[400px]">
        {viewMode === 'grid' ? (
          // GRID VIEW (4:5 Aspect Ratio)
          <div className="grid grid-cols-3 gap-0.5">
            {allPosts.map((post) => (
              <div key={post.uniqueId} className="aspect-[4/5] bg-gray-100 relative group overflow-hidden">
                <div className="absolute inset-0">
                  {/* OVERRIDE CANVAS WITH CURRENT BRAND CONFIG FOR LIVE PREVIEW */}
                  <Canvas 
                    key={`${brandConfig?.colors.primary}-${brandConfig?.typography.fontFamily}-${showShifter}`}
                    data={{
                        ...post,
                        slideNumber: undefined,
                        // Override logic: Use global settings if Shifter is likely active or we want consistency
                        fontFamily: brandConfig?.typography?.fontFamily || post.fontFamily,
                        accentFontFamily: brandConfig?.typography?.accentFontFamily || post.accentFontFamily,
                        color: brandConfig?.colors?.primary || post.color,
                        backgroundColor: brandConfig?.colors?.background || post.backgroundColor,
                        secondaryColor: brandConfig?.colors?.secondary || post.secondaryColor,
                        accentColor: brandConfig?.colors?.accent || post.accentColor,
                    }} 
                    brandName={brandSettings.currentBrandConfig?.name} 
                  />
                </div>
                
                {/* Overlay for Extra Posts */}
                {post.isExtra && (
                  <button 
                    onClick={() => removePostFromFeed(post.id)}
                    className="absolute top-1 right-1 bg-red-500 text-white p-1 rounded-full opacity-0 group-hover:opacity-100 transition-opacity z-20"
                  >
                    <SafeIcon icon={FiTrash2} className="text-xs" />
                  </button>
                )}
                {post.isPlan && (
                  <div className="absolute bottom-1 right-1 bg-black/50 text-white text-[8px] px-1 rounded opacity-0 group-hover:opacity-100 z-20">
                    {post.dayTitle}
                  </div>
                )}
              </div>
            ))}
            
            {/* ADD BUTTON (LIBRARY) */}
            <button onClick={() => setShowLibrary(true)} className="aspect-[4/5] bg-gray-50 flex flex-col items-center justify-center text-gray-400 hover:bg-purple-50 hover:text-purple-600 transition-colors border border-gray-100">
              <SafeIcon icon={FiLayers} className="text-2xl mb-1" />
              <span className="text-[10px] font-bold text-center px-1">Library</span>
            </button>
            
            {/* QUICK UPLOAD BUTTON */}
            <label className="aspect-[4/5] bg-gray-50 flex flex-col items-center justify-center text-gray-400 hover:bg-blue-50 hover:text-blue-600 transition-colors cursor-pointer border border-gray-100">
              <SafeIcon icon={FiUpload} className="text-2xl mb-1" />
              <span className="text-[10px] font-bold text-center px-1">Foto</span>
              <input type="file" accept="image/*" onChange={handleQuickPostUpload} className="hidden" />
            </label>
          </div>
        ) : (
          // LIST VIEW (Timeline - Full 4:5)
          <div className="flex flex-col space-y-8 p-0 pt-4">
            {allPosts.map((post) => (
              <div key={post.uniqueId} className="bg-white border-b border-gray-100 pb-4">
                <div className="flex items-center px-3 py-2">
                  <div className="w-8 h-8 rounded-full bg-gray-200 overflow-hidden mr-3">
                    {feedProfile.profileImage && <img src={feedProfile.profileImage} className="w-full h-full object-cover" />}
                  </div>
                  <span className="font-bold text-sm">{feedProfile.username}</span>
                </div>
                <div className="w-full aspect-[4/5] bg-gray-100 relative">
                  <div className="absolute inset-0">
                    {/* OVERRIDE CANVAS HERE TOO */}
                    <Canvas 
                        key={`list-${brandConfig?.colors.primary}-${brandConfig?.typography.fontFamily}`}
                        data={{
                            ...post,
                            slideNumber: undefined,
                            fontFamily: brandConfig?.typography?.fontFamily || post.fontFamily,
                            accentFontFamily: brandConfig?.typography?.accentFontFamily || post.accentFontFamily,
                            color: brandConfig?.colors?.primary || post.color,
                            backgroundColor: brandConfig?.colors?.background || post.backgroundColor,
                            secondaryColor: brandConfig?.colors?.secondary || post.secondaryColor,
                            accentColor: brandConfig?.colors?.accent || post.accentColor,
                        }} 
                        brandName={brandSettings.currentBrandConfig?.name} 
                    />
                  </div>
                </div>
                <div className="px-3 py-2">
                  <div className="flex space-x-4 text-2xl mb-2">
                    <SafeIcon icon={FiHeart} />
                    <SafeIcon icon={FiMessageCircle} />
                    <SafeIcon icon={FiSend} />
                  </div>
                  <div className="text-sm">
                    <span className="font-bold mr-2">{feedProfile.username}</span>
                    {post.text ? post.text.substring(0, 60) + "..." : "Caption..."}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* LIBRARY MODAL */}
      <AnimatePresence>
        {showLibrary && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-end sm:items-center justify-center p-4"
          >
            <motion.div 
              initial={{ y: 100 }}
              animate={{ y: 0 }}
              exit={{ y: 100 }}
              className="bg-white w-full max-w-sm rounded-xl overflow-hidden h-3/4 flex flex-col shadow-2xl"
            >
              <div className="p-4 border-b border-gray-100 flex justify-between items-center">
                <h3 className="font-bold">Add from Library</h3>
                <button onClick={() => setShowLibrary(false)}><SafeIcon icon={FiX} /></button>
              </div>
              <div className="flex-1 overflow-y-auto p-4 grid grid-cols-2 gap-4">
                {savedDesigns.length === 0 && (
                  <div className="col-span-2 text-center text-gray-500 py-10">
                    <p className="text-sm">Keine Designs gespeichert.</p>
                    <Link to="/create" className="text-purple-600 text-xs font-bold mt-2 inline-block">Erstelle eins!</Link>
                  </div>
                )}
                {savedDesigns.map(design => {
                  const previewSlide = design.isCollection ? design.slides[0] : design;
                  return (
                    <button 
                      key={design.id} 
                      onClick={() => { addPostToFeed(previewSlide); setShowLibrary(false); }}
                      className="aspect-[4/5] bg-gray-100 rounded overflow-hidden relative border border-gray-200 hover:ring-2 hover:ring-purple-500 transition-all"
                    >
                      <div className="w-full h-full pointer-events-none">
                        <Canvas data={{...previewSlide, slideNumber: undefined}} brandName={brandSettings.currentBrandConfig?.name} />
                      </div>
                      {design.isCollection && (
                        <div className="absolute top-1 right-1 bg-black/60 text-white rounded px-1 text-[8px] flex items-center">
                          <SafeIcon icon={FiLayers} className="mr-1" /> {design.slides.length}
                        </div>
                      )}
                    </button>
                  );
                })}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default FeedPreview;