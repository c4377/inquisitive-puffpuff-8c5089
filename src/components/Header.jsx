import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
// FIX: Named imports to prevent crash
import { FiHome, FiShuffle, FiPlus, FiSettings, FiZap, FiCalendar, FiEdit3, FiMenu, FiX, FiChevronRight, FiGrid, FiUsers, FiSmartphone, FiLogOut, FiLogIn, FiFileText } from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { useBrand } from '../context/BrandContext';
import { useAuth } from '../context/AuthContext';

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { brandSettings } = useBrand();
  const { user, signOut } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  // Safely check for brand configuration existence
  const hasActiveBrand = brandSettings?.currentBrandConfig || (brandSettings?.brandConfigurations?.length > 0);

  const navItems = [
    { path: '/', icon: FiHome, label: 'Dashboard' },
    { path: '/brand-randomizer', icon: FiShuffle, label: 'Randomizer' },
    { path: '/content-planner', icon: FiCalendar, label: 'Posts', disabled: !hasActiveBrand },
    { path: '/story-planner', icon: FiSmartphone, label: 'Stories', disabled: !hasActiveBrand },
    // NEW WORKSHEETS LINK
    { path: '/worksheets', icon: FiFileText, label: 'Worksheets', disabled: !hasActiveBrand },
    { path: '/community-planner', icon: FiUsers, label: 'Community', disabled: !hasActiveBrand },
    { path: '/feed-preview', icon: FiGrid, label: 'Feed', disabled: !hasActiveBrand },
    { path: '/create', icon: FiPlus, label: 'Create', disabled: !hasActiveBrand },
    { path: '/brand-settings', icon: FiSettings, label: 'Settings' }
  ];

  const closeMenu = () => setIsMobileMenuOpen(false);

  const handleSignOut = async () => {
    await signOut();
    closeMenu();
    navigate('/login');
  };

  return (
    <motion.header
      className="fixed top-0 w-full bg-white/90 backdrop-blur-md border-b border-gray-200 z-50"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2 z-50 relative" onClick={closeMenu}>
            <div className="w-8 h-8 bg-gradient-to-br from-purple-600 to-pink-600 rounded-lg flex items-center justify-center shadow-sm">
              <SafeIcon icon={FiZap} className="text-white text-lg" />
            </div>
            <span className="font-bold text-xl text-gray-900 tracking-tight">BrandStudio</span>
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex space-x-1">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path;
              if (item.disabled) {
                return (
                  <div key={item.path} className="flex items-center space-x-2 px-3 py-2 text-gray-400 cursor-not-allowed opacity-50">
                    <SafeIcon icon={item.icon} className="text-lg" />
                    <span className="font-medium text-sm hidden xl:inline">{item.label}</span>
                  </div>
                );
              }
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg transition-all duration-200 ${isActive
                    ? 'bg-purple-50 text-purple-700 font-semibold'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                  title={item.label}
                >
                  <SafeIcon icon={item.icon} className="text-lg" />
                  <span className="font-medium text-sm hidden xl:inline">{item.label}</span>
                </Link>
              );
            })}
          </nav>

          <div className="hidden md:flex items-center space-x-4">
            {user ? (
              <div className="flex items-center space-x-3">
                <span className="text-xs text-gray-500 font-medium hidden lg:block">{user.email}</span>
                <button
                  onClick={handleSignOut}
                  className="bg-gray-900 text-white px-4 py-2 rounded-lg font-medium hover:bg-gray-800 transition-all duration-200 text-sm shadow-sm flex items-center"
                >
                  <SafeIcon icon={FiLogOut} className="mr-2" /> Logout
                </button>
              </div>
            ) : (
              <Link
                to="/login"
                className="bg-gray-900 text-white px-4 py-2 rounded-lg font-medium hover:bg-gray-800 transition-all duration-200 text-sm shadow-sm flex items-center"
              >
                <SafeIcon icon={FiLogIn} className="mr-2" /> Login
              </Link>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden z-50 flex items-center">
            <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="p-2 text-gray-600 hover:text-gray-900 focus:outline-none">
              <SafeIcon icon={isMobileMenuOpen ? FiX : FiMenu} className="text-2xl" />
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Overlay */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'calc(100vh - 64px)' }} // FIXED: Subtract header height to fit viewport perfectly
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="md:hidden fixed inset-0 top-16 bg-white z-40 overflow-y-auto"
          >
            <div className="px-4 py-6 space-y-4 flex flex-col min-h-full pb-24"> {/* FIXED: min-h-full allows scrolling if content pushes boundaries */}
              {user && (
                <div className="bg-purple-50 p-4 rounded-xl mb-4 border border-purple-100">
                  <p className="text-xs text-purple-600 font-bold uppercase mb-1">Eingeloggt als</p>
                  <p className="text-sm font-bold text-gray-900">{user.email}</p>
                </div>
              )}
              {navItems.map((item) => {
                if (item.disabled) return null;
                const isActive = location.pathname === item.path;
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={closeMenu}
                    className={`flex items-center space-x-4 px-4 py-4 rounded-xl text-lg font-medium transition-colors ${isActive
                      ? 'bg-purple-50 text-purple-700 border border-purple-100'
                      : 'text-gray-600 hover:bg-gray-50'
                      }`}
                  >
                    <div className={`p-2 rounded-lg ${isActive ? 'bg-purple-100' : 'bg-gray-100'}`}>
                      <SafeIcon icon={item.icon} className="text-xl" />
                    </div>
                    <span>{item.label}</span>
                  </Link>
                );
              })}
              <div className="mt-auto border-t border-gray-100 pt-6 space-y-3">
                {user ? (
                  <button
                    onClick={handleSignOut}
                    className="w-full bg-gray-200 text-gray-800 py-4 rounded-xl font-bold text-lg shadow-sm flex items-center justify-center"
                  >
                    <SafeIcon icon={FiLogOut} className="mr-2" /> Logout
                  </button>
                ) : (
                  <Link
                    to="/login"
                    onClick={closeMenu}
                    className="w-full bg-gray-900 text-white flex items-center justify-center py-4 rounded-xl font-bold text-lg shadow-lg"
                  >
                    <SafeIcon icon={FiLogIn} className="mr-2" /> Login / Signup
                  </Link>
                )}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.header>
  );
};

export default Header;