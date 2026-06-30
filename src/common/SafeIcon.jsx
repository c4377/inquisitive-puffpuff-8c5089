import React from 'react';
import { FiAlertTriangle } from 'react-icons/fi';

const SafeIcon = ({ icon, name, className, ...props }) => {
  let IconComponent = icon;

  // Fallback if icon is missing or invalid
  if (!IconComponent || typeof IconComponent !== 'function') {
    return (
      <FiAlertTriangle 
        {...props} 
        className={`text-yellow-500 ${className || ''}`} 
        title="Icon not found" 
      />
    );
  }

  return <IconComponent className={className} {...props} />;
};

export default SafeIcon;