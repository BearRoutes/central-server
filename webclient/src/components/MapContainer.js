import React, { Component } from 'react';
import Dot from './Dot';

const mapWidthInPixels = 1791;
const mapHeightInPixels = 1484;

const heatmap = {"heat":{"2-125":66,"2-118":0,"2-117":66,"STR-1":0,"2-002ZZ":3,"ELV-179":19,"2-132":0,"AST-8":0,"2-001":1,"Pedway":2,"2-001ZZA":0,"2-003":23,"2-011":44,"STR-6":4,"STR-2":66,"2-005ZZB":43,"ELV-18X":19,"2-054":66,"2-047":16,"STR-4":23,"2-050":42,"2-052":0,"2-043":1,"2-048":30,"2-042":20,"2-039":20,"2-038":5,"2-037":41,"2-090":0,"2-060C":0,"2-005ZZA":0,"2-060B":0,"2-060A":0,"STR-5":0,"STR-3":1,"2-020":65,"2-016":30,"2-010":36,"2-001ZZD":66,"2-001ZZC":31,"2-001ZZB":9,"2-002":21,"AST-2-132":1,"2-127":44}}

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
    heats: {}
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
        this.setState({ heats: heatmap.heat})
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
    console.log()
    return (
      <div>
        <input type="file" onChange={this.handleFileSelect} />
        <button onClick={this.handleFileRead}>Add Dots</button>
        <div className="floor-map-container" style={{ width: `${mapWidthInPixels}px`, height: `${mapHeightInPixels}px`, position: 'relative' }}>
          <Lines dots = {this.state.dots} numNeighbors={this.state.numNeighbors}/>
          <div className="dot-container" style={{width: '100%', height: '100%', position: 'absolute', left: '-397.5px', bottom: '-155px'}}>
            {this.state.dots.map((dot, index) => (
              <Dot key={index} name={dot.name} x={dot.x} y={dot.y} color={dot.color} heat={this.state.heats[dot.name]}/>
            ))}
          </div>
        </div>
      </div>
    );
  }
}

export default Container;

