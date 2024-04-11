import React, { useState, useEffect } from 'react';
import './App.css';
import Container from './components/MapContainer';
import NavigationBar from './components/NavBar';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

function App() {
  const [zoomLevel, setZoomLevel] = useState(1);
  const [dots, setDots] = useState([]);
  const [routeData, setRouteData] = useState(null);
  const [startPoint, setStartPoint] = useState('');
  const [endPoint, setEndPoint] = useState('');
  // Function to add a new dot
  const addDot = (x, y, color = 'red') => {
    const newDot = { x, y, color };
    setDots(currentDots => [...currentDots, newDot]);
  };

  const fetchRouteData = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/route?start=${startPoint}&end=${endPoint}`);
      setRouteData(response.data.route);
    } catch (error) {
      console.error('Error fetching route data:', error);
    }
  };

  useEffect(() => {
    if (startPoint && endPoint) {
      fetchRouteData();
    }
  }, [startPoint, endPoint]);

  return (
    <div className="App">
      <NavigationBar 
        setStartPoint={setStartPoint}
        setEndPoint={setEndPoint}
        startPoint={startPoint}
        endPoint={endPoint}
      />
      <Container 
        zoomLevel={zoomLevel} 
        setZoomLevel={setZoomLevel}
        dots={dots} // Pass the dots as props
        routeData={routeData}
        startPoint={startPoint}
        endPoint={endPoint}
      />
    </div>
  );
}

export default App;
