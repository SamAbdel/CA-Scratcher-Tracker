import React, { useState, useEffect } from 'react';


const ScratchersTable = () => {
  const [scratchersData, setScratchersData] = useState([]);

  // Fetch data from the API
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/scratchers/best-odds?prices=1,2,3,5,10,20,30');
        const data = await response.json();
        setScratchersData(data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>Scratchers Table</h2>
      <h2>Scratchers Table</h2>
      <table>
        <thead>
          <tr>
            <th></th>
            <th>Name</th>
            <th>Price</th>
            <th>Odds to Win Cash Prize (Out of 1)</th>
          </tr>
        </thead>
        <tbody>
          {/* Render table rows with the fetched data */}
          {scratchersData.map((scratcher, index) => (
            <tr key={index}>
              <td><img src={scratcher.img_source} alt={scratcher.name} /></td>
              <td>{scratcher.scratcher_name}</td>
              <td>${scratcher.price}</td>
              <td>{scratcher.odds}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ScratchersTable;
