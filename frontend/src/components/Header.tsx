import React from 'react';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-section">
          <div className="logo-icon">📋</div>
          <div className="brand-info">
            <h1 className="header-title">Compliance Auditor AI</h1>
            <p className="header-subtitle">AI-Powered Document Verification System</p>
          </div>
        </div>
        <div className="header-features">
          <span className="feature-tag">Secure</span>
          <span className="feature-tag">AI-Powered</span>
          <span className="feature-tag">Real-time</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
