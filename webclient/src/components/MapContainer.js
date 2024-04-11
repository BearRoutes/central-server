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
    heats: {},
    selectedDay: 0,
    selectedHour: 7
  };

  constructor(props) {
    super(props);
    // Bind methods
    this.handleFileSelect = this.handleFileSelect.bind(this);
    this.handleDayChange = this.handleDayChange.bind(this);
    this.handleHourChange = this.handleHourChange.bind(this);
    this.updateHeatData = this.updateHeatData.bind(this);
    this.showCurrentHeatData = this.showCurrentHeatData.bind(this);
  }

  handleDayChange(event) {
    this.setState({ selectedDay: parseInt(event.target.value) });
  }

  handleHourChange(event) {
    this.setState({ selectedHour: parseInt(event.target.value) });
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
      const hour = currentDate.getHours()
      const dayOfWeek = currentDate.getDay()
      const month = currentDate.getMonth() + 1
      const heatResponse = await axios.get(`http://localhost:8000/heat?month=${month}&day=${dayOfWeek}&hour=${hour}`);
      
      // Update state with fetched data
      this.setState({
        heats: heatResponse.data,
        selectedDay: dayOfWeek,
        selectedHour: hour,
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

  async updateHeatData() {
    try {
      const currentDate = new Date();
      const month = currentDate.getMonth() + 1
      const { selectedDay, selectedHour } = this.state;
      const heatResponse = await axios.get(`http://localhost:8000/heat?month=${month}&day=${selectedDay}&hour=${selectedHour}`);
      
      // Update state with fetched data
      this.setState({
        heats: heatResponse.data
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }

  async showCurrentHeatData () {
    try {
      const currentDate = new Date();
      const hour = currentDate.getHours()
      const dayOfWeek = currentDate.getDay()
      const month = currentDate.getMonth() + 1
      const heatResponse = await axios.get(`http://localhost:8000/heat?month=${month}&day=${dayOfWeek}&hour=${hour}`);
      
      // Update state with fetched data
      this.setState({
        heats: heatResponse.data,
        selectedDay: dayOfWeek,
        selectedHour: hour,
      });
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }


  render() {
    const {showLines, selectedDay, selectedHour} = this.state;
    console.log()
    return (
      <div>
        <div>
          <label>Select Day:</label>
          <select value={selectedDay} onChange={this.handleDayChange}>
            <option value={0}>Sunday</option>
            <option value={1}>Monday</option>
            <option value={2}>Tuesday</option>
            <option value={3}>Wednesday</option>
            <option value={4}>Thursday</option>
            <option value={5}>Friday</option>
            <option value={6}>Saturday</option>
          </select>
          <label>Select Hour:</label>
          <select value={selectedHour} onChange={this.handleHourChange}>
            {[...Array(13).keys()].map(hour => (
              <option key={hour} value={hour + 7}>{hour + 7}:00</option>
            ))}
          </select>
          <button onClick={this.updateHeatData}>Update Heat Data</button>
          <button onClick={this.showCurrentHeatData}>Show Current Heat Data</button>
        </div>
        
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

