import React, { Component } from 'react';
import Dot from './Dot';
import axios from 'axios';

const mapWidthInPixels = 1791;
const mapHeightInPixels = 1484;

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

  handleShowRoute = async () => {
    const { fileRead } = this.state;
    if (fileRead && this.props.startPoint && this.props.endPoint) {
      const start = this.props.startPoint.split(' ')[1];
      const end = this.props.endPoint.split(' ')[1];
      const url = `http://localhost:8000/route?start=${start}&end=${end}`
      const routeNames = await axios.get(url);
      if (routeNames.data?.route.length > 0) {
        const routeDots = routeNames.data?.route.map(name => this.state.dots.find(dot => dot.name === name)).filter(dot => dot);
        this.setState({ routeDots });
        // Assuming routeDots is calculated somewhere after reading the file
        this.setState((prevState) => ({ showLines: !prevState.showLines }));
      }
    } else {
      alert('Please add the HeatMap first.');
    }
  };

  async componentDidMount() {
    try {
      const currentDate = new Date();
      const formattedDate = currentDate.toISOString(); // Convert to ISO format
      const heatResponse = await axios.get(`http://localhost:8000/heat?timestamp=${formattedDate}`);
      
      // Update state with fetched data
      this.setState({
        heats: heatResponse.data.heat
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }

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

        this.setState({ dots: newDots })

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

