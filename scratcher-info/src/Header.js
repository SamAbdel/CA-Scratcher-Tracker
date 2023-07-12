import React from 'react';
import './Header.css'

const Header = () => {
    return (
      <header className="header-container">
        <div className="header-title">
          CA Lottery Tracker
        </div>
        <div className="header-links">
          <a href="/all-scratchers">All Scratchers</a>
          <a href="/more-info">More Info</a>
          <a href="https://example.com">CA Lottery Main Site</a>
        </div>
      </header>
    );
  };
export default Header;