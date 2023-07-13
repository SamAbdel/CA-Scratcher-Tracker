import './App.css';
import AllScratchersTable from './AllScratchersTable';
import About from './About';
import ScratchersTable from './ScratchersTable';
import Header from './Header';
import React, { useEffect, useState } from 'react';

const App = () => {
  const [currentUrl, setCurrentUrl] = useState(window.location.pathname);

  useEffect(() => {
    const handleUrlChange = () => {
      setCurrentUrl(window.location.pathname);
    };

    window.addEventListener('popstate', handleUrlChange);
    return () => {
      window.removeEventListener('popstate', handleUrlChange);
    };
  }, []);

  const renderPage = () => {
    if (currentUrl === '/About') {
      return <About />;
    }
    if (currentUrl === '/all-scratchers') {
      return <AllScratchersTable />;
    }
    // Render other pages/components based on the current URL
    // Add your routing logic here
    // For example:
    // if (currentUrl === '/some-other-page') {
    //   return <SomeOtherPage />;
    // }
    return null;
  };

  return (
    <div className="main-menu">
      <Header />
      {currentUrl !== '/About' && currentUrl !== '/all-scratchers' && <ScratchersTable />}
      {renderPage()}
    </div>
  );
};

export default App;
