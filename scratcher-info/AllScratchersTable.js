import React, { useState, useEffect } from 'react';

const AllScratchersTable = () => {
  const [scratchersData, setScratchersData] = useState([]);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch data from the API
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/scratchers');
        const data = await response.json();
        setScratchersData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const handleSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const sortedData = [...scratchersData].sort((a, b) => {
    if (sortConfig.direction === 'ascending') {
      return a[sortConfig.key] - b[sortConfig.key];
    } else {
      return b[sortConfig.key] - a[sortConfig.key];
    }
  });

  const filteredData = sortedData.filter((scratcher) =>
    scratcher.scratcher_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  return (
    <div>
      <h2>Scratchers Table</h2>
      <div className="search-bar">
        <input type="text" value={searchQuery} onChange={handleSearchChange} placeholder="Search by Name" />
      </div>
      <table>
        <thead>
          <tr>
            <th></th>
            <th onClick={() => handleSort('scratcher_name')}>
              Name {sortConfig.key === 'scratcher_name' && (sortConfig.direction === 'ascending' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('price')}>
              Price {sortConfig.key === 'price' && (sortConfig.direction === 'ascending' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('odds')}>
              Odds to Win Cash Prize (Out of 1) {sortConfig.key === 'odds' && (sortConfig.direction === 'ascending' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('Top_Prize')}>
              Top Prize {sortConfig.key === 'Top_Prize' && (sortConfig.direction === 'ascending' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('Top_Prizes_Left')}>
              Top Prizes Left {sortConfig.key === 'Top_Prizes_Left' && (sortConfig.direction === 'ascending' ? '↑' : '↓')}
            </th>
            <th onClick={() => handleSort('Top_Prize_Odds')}>
              Top Prize Odds: 1 in {sortConfig.key === 'Top_Prize_Odds' && (sortConfig.direction === 'ascending' ? '↑' : '↓')}
            </th>
          </tr>
        </thead>
        <tbody>
          {filteredData.map((scratcher, index) => (
            <tr key={index}>
              <td><img src={scratcher.img_source} alt={scratcher.name} /></td>
              <td>{scratcher.scratcher_name}</td>
              <td>${scratcher.price}</td>
              <td>{scratcher.odds}</td>
              <td>${scratcher.Top_Prize}</td>
              <td>{scratcher.Top_Prizes_Left}</td>
              <td>{scratcher.Top_Prize_Odds}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AllScratchersTable;
