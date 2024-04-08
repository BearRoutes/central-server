import React, { Component } from 'react';
import Dot from './Dot';

const mapWidthInPixels = 1791;
const mapHeightInPixels = 1484;

function getDistance(dot1, dot2) {
  return Math.sqrt((dot1.x - dot2.x) ** 2 + (dot1.y - dot2.y) ** 2);
}

function findClosestNeighbors(dots, numNeighbors = 3) {
  return dots.map(dot => {
    // Create a list of all other dots with their distances to the current dot
    let allDotsWithDistances = dots
      .filter(compareDot => compareDot !== dot) // Exclude the current dot
      .map(compareDot => ({
        compareDot,
        distance: getDistance(dot, compareDot)
      }));
    
    // Sort by distance
    allDotsWithDistances.sort((a, b) => a.distance - b.distance);

    // Take the closest numNeighbors dots
    let closestNeighbors = allDotsWithDistances.slice(0, numNeighbors).map(d => d.compareDot);

    return { dot, neighbors: closestNeighbors };
  });
}

const Lines = ({ dots, numNeighbors }) => {
  const dotNeighbors = findClosestNeighbors(dots, numNeighbors);

  return (
    <svg style={{ position: 'absolute', left: '-397.5px', bottom: '-155px', width: '100%', height: '100%' }}>
      {dotNeighbors.flatMap(({ dot, neighbors }) => 
        neighbors.map((neighbor, index) => (
          <line
            key={`${dot.name}-${neighbor.name}-${index}`}
            x1={dot.x}
            y1={dot.y}
            x2={neighbor.x}
            y2={neighbor.y}
            stroke="rgba(0,0,0,0.4)" //change to rgba(0,0,0,0) for transparent lines
            strokeWidth="1"
          />
        ))
      )}
    </svg>
  );
};


class Container extends Component {
  state = {
    dots: [],
    connection: [],
    selectedFile: null,
  };

  constructor(props) {
    super(props);
    // Bind methods
    this.handleFileSelect = this.handleFileSelect.bind(this);
    this.handleFileRead = this.handleFileRead.bind(this);
  }

  componentDidMount() {
    // Adding event listener when the component mounts
    const container = document.querySelector('.floor-map-container');
    container.addEventListener('wheel', this.handleWheel, { passive: false });
  }

  componentWillUnmount() {
    // Removing event listener when the component unmounts
    const container = document.querySelector('.floor-map-container');
    container.removeEventListener('wheel', this.handleWheel);
  }

  handleFileSelect(event) {
    if (event.target.files && event.target.files[0]) {
      this.setState({ selectedFile: event.target.files[0] });
    } else {
      console.error('No file was selected.');
    }
  }

  handleFileRead() {
    const { selectedFile } = this.state;
    if (selectedFile) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target.result;
        const lines = text.split('\n');
        const newDots = lines.map((line) => {
          const [nameStr, xStr, yStr, color] = line.split(',');

          const x = parseFloat(xStr)*20.2;
          const y = mapHeightInPixels - parseFloat(yStr)*20.2;
          const name = nameStr;
                  
          console.log(name, x, y)
          if (!isNaN(x) && !isNaN(y)) {
            return { name, x, y, color: color || 'red' }; // Default to red if color is not specified
          } else {
            console.error('Invalid format in line:', line);
            return null;
          }
        }).filter(dot => dot); // Remove null values

        this.setState({ dots: newDots });
      };
      reader.onerror = () => {
        console.error('Error reading file.');
      };
      reader.readAsText(selectedFile);
    } else {
      console.error('No file is selected to read.');
    }
  }

  render() {
    return (
      <div>
        <input type="file" onChange={this.handleFileSelect} />
        <button onClick={this.handleFileRead}>Add Dots</button>
        <div className="floor-map-container" style={{ width: `${mapWidthInPixels}px`, height: `${mapHeightInPixels}px`, position: 'relative' }}>
          <Lines dots = {this.state.dots} numNeighbors={this.state.numNeighbors}/>
          <div className="dot-container" style={{width: '100%', height: '100%', position: 'absolute', left: '-397.5px', bottom: '-155px'}}>
            {this.state.dots.map((dot, index) => (
              <Dot key={index} name={dot.name} x={dot.x} y={dot.y} color={dot.color} />
            ))}
          </div>
        </div>
      </div>
    );
  }
}

export default Container;

