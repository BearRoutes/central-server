import React from 'react';
// Correct scale description to Pixels per Meter
const scale = 1791 / 10; // Pixels per Meter
const mapHeightInPixels = 1484; // Height of the map in pixels

// const Dot = ({ x, y, zoom, color }) => {

//   console.log(x, y);
//   const x_px = x * scale;
//   const y_px = mapHeightInPixels - (y * scale);

//   // Adjust dot size based on the zoom level. You can change the calculation as needed.
//   // For example, this makes the dot's size double as the zoom level goes from 1 to 2, and so on.
//   const baseSize = 30; // Base size of the dot without zoom
//   const size = baseSize ; // Adjust dot size based on zoom
//   console.log(x_px, y_px);

//   const dotStyle = {
//     position: 'absolute',
//     width: `${size}px`,
//     height: `${size}px`,
//     backgroundColor: color,
//     borderRadius: '50%',
//     // Adjust position to account for the changed size and ensure the dot remains centered
//     // You might want to adjust how zoom affects position if the zooming behavior doesn't look right
//     left: `calc(${x_px}px - ${size / 2}px)`, 
//     top: `calc(${y_px}px - ${size / 2}px)`,
//     transform: 'translate(-50%, -50%)',
//   };

//   return <div style={dotStyle}></div>;
// };

const Dot = ({ x, y, color }) => {
  return <div style={{ position: 'absolute', left: x, top: y, width: '10px', height: '10px', backgroundColor: color, borderRadius: '50%' }} />;
};

export default Dot;
