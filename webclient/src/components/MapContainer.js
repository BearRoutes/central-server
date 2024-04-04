import React, { Component } from 'react';
import Dot from './Dot';

const mapWidthInPixels = 1791;
const mapHeightInPixels = 1484;

class Container extends Component {
  constructor(props) {
    super(props);
    this.state = {
      dots: [],
      selectedFile : null,
    };
    // Binding this context to methods
    this.addDot = this.addDot.bind(this);
    this.handleWheel = this.handleWheel.bind(this);
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

  handleFileSelect(event){
    if (event.target.files && event.target.files[0]) {
      this.setState({ selectedFile: event.target.files[0] });
    } else {
      console.error('No file was selected.');
    }
  }

  handleFileRead(){
    const { selectedFile } = this.state;
    if (selectedFile) {
      const reader = new FileReader();

      reader.onload = (e) => {
        const text = e.target.result;
        const lines = text.split('\n');
        // Parse lines and add dots
        lines.forEach((line) => {
          const [xStr, yStr, color] = line.split(',');
          const x = parseFloat(xStr);
          const y = parseFloat(yStr);
          // Ensure x and y are numbers and color is a string
          if (!isNaN(x) && !isNaN(y) && color) {
            this.addDot(x, y, color);
          } else {
            console.error('Invalid format in line:', line);
          }
        });
      };

      reader.onerror = (e) => {
        console.error('Error reading file:', e);
      };

      reader.readAsText(selectedFile);
    } else {
      console.error('No file is selected to read.');
    }
  }


  handleWheel(e) {
    // e.preventDefault();
    // const zoomLevel = this.props.zoomLevel;
    // const setZoomLevel = this.props.setZoomLevel;
    // const newZoomLevel = e.deltaY < 0 ? Math.min(zoomLevel + 0.1, 3) : Math.max(zoomLevel - 0.1, 0.5);
    // setZoomLevel(newZoomLevel);
  }

  addDot(x, y, color) {

    // const inverted_y = mapHeightInPixels-y;

    const newDot = { x, y, color };
    console.log('Adding new dot:', newDot);
    this.setState(prevState => {
    const newState = { dots: [...prevState.dots, newDot] };
    console.log('New state:', newState);
    return newState;
  });
  }

  render() {
    const {dots } = this.props;
    return (
        <div>

          <input type="file" onChange={this.handleFileSelect} />
          <button onClick={this.handleFileRead}>Add Dots</button>

          <div className="floor-map-container" style={{ width: `${mapWidthInPixels}px`, height: `${mapHeightInPixels}px`, position: 'relative' }}>
            <Dot x={100} y={100} color="red" />
            {dots.map((dot, index) => (
              <Dot x={dot.x} y={dot.y}  color={dot.color} />
            ))}
          </div>
        </div>
      );
  }
}

export default Container;
