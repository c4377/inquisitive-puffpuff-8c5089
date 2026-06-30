import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import * as FiIcons from 'react-icons/fi';
import SafeIcon from '../common/SafeIcon';
import { useBrand } from '../context/BrandContext';

const { FiZap, FiLayout, FiPlus, FiTrendingUp, FiImage, FiCheck, FiArrowRight, FiCalendar, FiEdit3 } = FiIcons;

const Dashboard = () => {
    const { brandSettings } = useBrand();
    const hasActiveBrand = brandSettings.currentBrandConfig || brandSettings.brandConfigurations?.length > 0;
    const currentBrand = brandSettings.currentBrandConfig;
    const hasPlan = brandSettings.contentPlan && brandSettings.contentPlan.length > 0;

    const quickActions = [
        { title: '1. Brand Randomizer', description: 'Create or choose your Brand Style', icon: FiZap, color: 'from-purple-500 to-pink-500', link: '/brand-randomizer', completed: hasActiveBrand },
        { title: '2. Content Planner', description: 'Create a 7-Day Content Plan', icon: FiCalendar, color: 'from-emerald-500 to-teal-500', link: '/content-planner', disabled: !hasActiveBrand, completed: hasPlan, highlight: true },
        { title: '3. Create Content', description: 'Design Single Posts & Stories', icon: FiPlus, color: 'from-orange-500 to-red-500', link: '/create', disabled: !hasActiveBrand }
    ];

    const stats = [
        { label: 'Saved Brands', value: brandSettings.brandConfigurations?.length || 0, icon: FiZap },
        { label: 'Content Plan', value: hasPlan ? 'Active' : 'Open', icon: FiCalendar },
        { label: 'Assets', value: (brandSettings.brandImages || []).length, icon: FiImage },
        { label: 'Brand Consistency', value: '98%', icon: FiTrendingUp }
    ];

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Hero Section */}
            <motion.div
                className="text-center mb-12"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
            >
                <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
                    Create Premium <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Instagram Content</span>
                </h1>
                <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                    Automatically generate Instagram posts in your visual branding. Professional, clean, and ready-to-post.
                </p>
            </motion.div>

            {/* ACTIVE BRAND CARD */}
            {currentBrand && (
                <motion.div
                    className="mb-12 bg-white rounded-2xl p-6 shadow-md border border-gray-100 flex flex-col md:flex-row items-center gap-6"
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.1 }}
                >
                    {/* LIVE MINI PREVIEW (4:5 post mockup) */}
                    <div
                        className="shrink-0 w-32 md:w-36 aspect-[4/5] rounded-xl shadow-inner border border-black/5 flex items-center justify-center p-4 overflow-hidden"
                        style={{ backgroundColor: currentBrand.colors?.background || '#ffffff' }}
                    >
                        <div
                            className="text-center leading-tight"
                            style={{
                                color: currentBrand.colors?.primary || '#111827',
                                fontFamily: `'${currentBrand.typography?.fontFamily || 'Inter'}', sans-serif`,
                            }}
                        >
                            <span className="block text-sm md:text-base font-bold uppercase tracking-tight">
                                Klarheit durch
                            </span>
                            <span
                                className="block text-sm md:text-base font-bold italic"
                                style={{ color: currentBrand.colors?.accent || currentBrand.colors?.secondary || '#888' }}
                            >
                                Fokus.
                            </span>
                        </div>
                    </div>

                    {/* INFO + PALETTE */}
                    <div className="flex-1 w-full">
                        <h3 className="text-lg font-bold text-gray-900">
                            Active Brand: {currentBrand.name}
                        </h3>
                        <p className="text-sm text-gray-500 mb-3">
                            {currentBrand.typography?.fontFamily}
                            {currentBrand.typography?.bodyFontFamily ? ` + ${currentBrand.typography.bodyFontFamily}` : ''}
                            {currentBrand.ruleSet ? ` • ${currentBrand.ruleSet}` : ''}
                        </p>

                        {/* Color palette as bars */}
                        <div className="flex rounded-lg overflow-hidden h-8 w-full max-w-xs shadow-sm border border-gray-100">
                            {Object.values(currentBrand.colors || {}).slice(0, 5).map((c, i) => (
                                <div key={i} className="flex-1" style={{ backgroundColor: c }} title={c} />
                            ))}
                        </div>
                    </div>

                    {/* ACTIONS */}
                    <div className="flex md:flex-col gap-3 shrink-0">
                        <Link to="/brand-settings" className="px-4 py-2 border border-gray-200 rounded-lg text-sm font-bold text-gray-700 hover:bg-gray-50 text-center">
                            Settings
                        </Link>
                        <Link to="/brand-randomizer" className="px-4 py-2 bg-purple-50 text-purple-700 rounded-lg text-sm font-bold hover:bg-purple-100 text-center">
                            Switch
                        </Link>
                    </div>
                </motion.div>
            )}

            {/* Workflow Steps */}
            <motion.div
                className="mb-12"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
            >
                <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-xl p-8">
                    <h2 className="text-2xl font-bold text-purple-900 mb-6 text-center">Your Workflow</h2>
                    <div className="grid md:grid-cols-3 gap-6">
                        {quickActions.map((action, index) => (
                            <Link
                                key={index}
                                to={action.link}
                                className={`group relative overflow-hidden bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 ${action.disabled ? 'opacity-50 cursor-not-allowed' : 'transform hover:-translate-y-2'} ${action.highlight ? 'ring-2 ring-emerald-400' : ''}`}
                            >
                                {action.completed && (
                                    <div className="absolute top-4 right-4 bg-green-500 text-white p-1 rounded-full z-10">
                                        <SafeIcon icon={FiCheck} className="text-sm" />
                                    </div>
                                )}
                                <div className={`absolute inset-0 bg-gradient-to-br ${action.color} opacity-0 group-hover:opacity-5 transition-opacity duration-300`}></div>
                                <div className="relative z-10">
                                    <div className="text-sm font-medium text-purple-600 mb-2">Step {index + 1}</div>
                                    <div className={`w-16 h-16 bg-gradient-to-br ${action.color} rounded-2xl flex items-center justify-center mb-6 shadow-md`}>
                                        <SafeIcon icon={action.icon} className="text-2xl text-white" />
                                    </div>

                                    <h3 className="text-xl font-bold text-gray-900 mb-2">{action.title}</h3>
                                    <p className="text-gray-600 mb-4">{action.description}</p>

                                    {!action.disabled && (
                                        <div className="flex items-center text-purple-600 font-medium group-hover:translate-x-1 transition-transform">
                                            <span>{action.completed ? 'Open' : 'Start'}</span>
                                            <SafeIcon icon={FiArrowRight} className="ml-2" />
                                        </div>
                                    )}
                                    {action.disabled && (
                                        <div className="text-sm text-gray-500 flex items-center">
                                            <SafeIcon icon={FiZap} className="mr-1" /> Create Brand First
                                        </div>
                                    )}
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
            </motion.div>

            {/* Stats */}
            <motion.div
                className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-12"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
            >
                {stats.map((stat, index) => (
                    <div key={index} className="bg-white rounded-xl p-6 text-center shadow-md border border-gray-100">
                        <SafeIcon icon={stat.icon} className="text-3xl text-purple-600 mx-auto mb-3" />
                        <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
                        <div className="text-sm text-gray-600">{stat.label}</div>
                    </div>
                ))}
            </motion.div>

            {!hasActiveBrand && (
                <motion.div
                    className="text-center"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.8 }}
                >
                    <div className="bg-purple-600 text-white rounded-2xl p-8 shadow-xl">
                        <h3 className="text-2xl font-bold mb-4">Start Here</h3>
                        <p className="text-purple-100 mb-6 max-w-2xl mx-auto">
                            Begin your journey with the Brand Randomizer. Create a unique design in seconds.
                        </p>
                        <Link
                            to="/brand-randomizer"
                            className="inline-block bg-white text-purple-600 px-8 py-3 rounded-lg font-medium hover:shadow-lg transition-all duration-200"
                        >
                            Go to Brand Randomizer
                        </Link>
                    </div>
                </motion.div>
            )}
        </div>
    );
};

export default Dashboard;