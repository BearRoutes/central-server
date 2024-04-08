import React from 'react';
// Correct scale description to Pixels per Meter
const scale = 1791 / 10; // Pixels per Meter
const mapHeightInPixels = 1484; // Height of the map in pixels

const getColorFromHeat = (heat) => {
  // Convert heat to a value between 0 and 1
  const normalizedHeat = heat / 75;

  // Interpolate between blue, yellow, and red based on heat
  let r, g, b;
  if (normalizedHeat < 0.5) {
    r = Math.round(255 * (2 * normalizedHeat));
    g = 255;
    b = Math.round(255 * (1 - 2 * normalizedHeat));
  } else {
    r = 255;
    g = Math.round(255 * (2 - 2 * normalizedHeat));
    b = 0;
  }

  // Construct CSS color string
  return `rgb(${r}, ${g}, ${b})`;
};



const Dot = ({ name, x, y, color, heat }) => {

  // console.log(x, y);
  // const x_px = x * scale;
  // const y_px = mapHeightInPixels - (y * scale);
  const node_name = name;
  const node_heat = heat;
  const dotColor = getColorFromHeat(node_heat);
  const size = Math.min(15 + node_heat, 50);
  const dotStyle = {
    position: 'absolute',
    left: `${x}px`,
    top: `${y}px`,
    width: `${size}px`,
    height: `${size}px`,
    backgroundColor: dotColor,
    borderRadius: '50%',
    transform: 'translate(-50%, -50%)', // Centers the dot on (x, y)
  };

  const labelStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    color: 'black',
    fontSize: '12px',
  };

  return (
    <div style={dotStyle}>
      <div style={labelStyle}>
        {node_heat}
      </div>
    </div>
  );
};

export default Dot;
