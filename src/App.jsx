import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';

import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import BrandRandomizer from './components/BrandRandomizer';
import LayoutSelector from './components/LayoutSelector';
import CreateContent from './pages/CreateContent';
import Templates from './pages/Templates';
import BrandSettings from './pages/BrandSettings';
import ContentPlanner from './pages/ContentPlanner';
import CommunityPlanner from './pages/CommunityPlanner';
import StoryPlanner from './pages/StoryPlanner';
import ReelCoverPlanner from './pages/ReelCoverPlanner';
import Editor from './pages/Editor';
import FeedPreview from './pages/FeedPreview';
import Login from './pages/Login';
import WorksheetGenerator from './pages/WorksheetGenerator';
import ScrollToTop from './components/ScrollToTop';
import { BrandProvider } from './context/BrandContext';
import { AuthProvider } from './context/AuthContext';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <BrandProvider>
        <Router>
          <ScrollToTop />
          <div className="min-h-screen bg-gray-50">
            <Header />
            <motion.main
              className="pt-16"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/login" element={<Login />} />
                <Route path="/brand-randomizer" element={<BrandRandomizer />} />
                <Route path="/layout-selector" element={<LayoutSelector />} />
                <Route path="/create" element={<CreateContent />} />
                <Route path="/editor" element={<Editor />} />
                <Route path="/templates" element={<Templates />} />
                <Route path="/brand-settings" element={<BrandSettings />} />
                <Route path="/content-planner" element={<ContentPlanner />} />
                <Route path="/community-planner" element={<CommunityPlanner />} />
                <Route path="/story-planner" element={<StoryPlanner />} />
                <Route path="/reel-covers" element={<ReelCoverPlanner />} />
                <Route path="/feed-preview" element={<FeedPreview />} />
                <Route path="/worksheets" element={<WorksheetGenerator />} /> {/* NEW ROUTE */}
              </Routes>
            </motion.main>
          </div>
        </Router>
      </BrandProvider>
    </AuthProvider>
  );
}

export default App;