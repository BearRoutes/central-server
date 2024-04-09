import React, { Component } from 'react';
import Dot from './Dot';

const mapWidthInPixels = 1791;
const mapHeightInPixels = 1484;


const routeData = {
  "route": ["2-118", "2-117", "2-125", "2-127", "2-132", "AST-2-132", "2-002", "2-001ZZB", "2-001"]
};

const heatmap = {"heat":{"2-125":66,"2-118":0,"2-117":66,"STR-1":0,"2-002ZZ":3,"ELV-179":19,"2-132":0,"AST-8":0,"2-001":1,"Pedway":2,"2-001ZZA":0,"2-003":23,"2-011":44,"STR-6":4,"STR-2":66,"2-005ZZB":43,"ELV-18X":19,"2-054":66,"2-047":16,"STR-4":23,"2-050":42,"2-052":0,"2-043":1,"2-048":30,"2-042":20,"2-039":20,"2-038":5,"2-037":41,"2-090":0,"2-060C":0,"2-005ZZA":0,"2-060B":0,"2-060A":0,"STR-5":0,"STR-3":1,"2-020":65,"2-016":30,"2-010":36,"2-001ZZD":66,"2-001ZZC":31,"2-001ZZB":9,"2-002":21,"AST-2-132":1,"2-127":44}}

function getDistance(dot1, dot2) {
  return Math.sqrt((dot1.x - dot2.x) ** 2 + (dot1.y - dot2.y) ** 2);
}

const routeNames = routeData.route;

const Lines = ({ routeDots }) => {
  return (
    <svg style={{ position: 'absolute', left: '-397.5px', bottom: '-155px', width: '100%', height: '100%' }}>
      {routeDots.map((dot, index) => (
        index < routeDots.length - 1 && (
          <line
            key={`line-${dot.name}-${routeDots[index + 1].name}`}
            x1={dot.x}
            y1={dot.y}
            x2={routeDots[index + 1].x}
            y2={routeDots[index + 1].y}
            stroke="blue" 
            strokeWidth="4"
          />
        )
      ))}
    </svg>
  );
};

class Container extends Component {
  state = {
    dots: [],
    connection: [],
    selectedFile: null,
    fileRead: false,
    routeDots: [],
    showLines: false,
    heats: {}
  };

  constructor(props) {
    super(props);
    // Bind methods
    this.handleFileSelect = this.handleFileSelect.bind(this);
    this.handleFileRead = this.handleFileRead.bind(this);
  }

  // toggleLines = () => {
  //   this.setState(prevState => ({ showLines: !prevState.showLines }));
  // };

  handleShowRoute = () => {
    const { fileRead } = this.state;
    if (fileRead) {
      // Assuming routeDots is calculated somewhere after reading the file
      this.setState((prevState) => ({ showLines: !prevState.showLines }));
    } else {
      alert('Please add the HeatMap first.');
    }
  };

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

  setRouteDots = (routeNames) => {
    const routeDots = routeNames.map(name => this.state.dots.find(dot => dot.name === name)).filter(dot => dot);
    this.setState({ routeDots });
  };

  handleFileSelect(event) {
    if (event.target.files && event.target.files[0]) {
      this.setState({ selectedFile: event.target.files[0] });
      this.setState({ fileRead: true });
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

        this.setRouteDots(routeNames);

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
    const {showLines} = this.state;
    console.log()
    return (
      <div>
        <input type="file" onChange={this.handleFileSelect} />
        <button onClick={this.handleFileRead} style={{ marginRight: '50px' }}>Add HeatMap</button>
        
        <button onClick={this.handleShowRoute}>
          {showLines ? 'Hide Lines' : 'Show Route'}
        </button>
        
        <div className="floor-map-container" style={{ width: `${mapWidthInPixels}px`, height: `${mapHeightInPixels}px`, position: 'relative' }}>
          
          {showLines && <Lines routeDots={this.state.routeDots} />}
        
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

