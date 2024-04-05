import React from 'react';
// Correct scale description to Pixels per Meter
const scale = 1791 / 10; // Pixels per Meter
const mapHeightInPixels = 1484; // Height of the map in pixels

const Dot = ({ name, x, y, color }) => {

  // console.log(x, y);
  // const x_px = x * scale;
  // const y_px = mapHeightInPixels - (y * scale);
  const node_name = name;
  
  const size = 15; // Size of the dot in pixels
  const dotStyle = {
    position: 'absolute',
    left: `${x}px`,
    top: `${y}px`,
    width: `${size}px`,
    height: `${size}px`,
    backgroundColor: color,
    borderRadius: '50%',
    transform: 'translate(-50%, -50%)', // Centers the dot on (x, y)
  };

  return <div style={dotStyle} />;
};

export default Dot;
