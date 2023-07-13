import React from 'react';
import './Header.css';

const Header = () => {
  const handleAboutClick = () => {
    window.location.href = '/About'; // Change the URL to the About page
  };

  return (
    <header className="header-container">
      <div className="header-title">
        CA Lottery Tracker
      </div>
      <div className="header-links">
        <a href="/all-scratchers">All Scratchers</a>
        <a href="#" onClick={handleAboutClick}>About</a> {/* Add onClick event handler */}
        <a href="https://example.com">CA Lottery Main Site</a>
      </div>
    </header>
  );
};

export default Header;
