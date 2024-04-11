import React, { Component } from 'react';
import Dot from './Dot';
import axios from 'axios';
import DotLocations from './config/DotLocations';

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
  }

  handleShowRoute = async () => {
    if (this.props.startPoint && this.props.endPoint) {
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
      alert('Please select a start and end point');
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
    this.setState({ dots: DotLocations })
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

  componentDidUpdate(prevProps) {
    // Check if startPoint or endPoint props have changed
    if (prevProps.startPoint !== this.props.startPoint || prevProps.endPoint !== this.props.endPoint) {
      this.setState({ showLines: false }); // Set showLines to false
    }
  }


  render() {
    const {showLines} = this.state;
    console.log()
    return (
      <div>
        
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

