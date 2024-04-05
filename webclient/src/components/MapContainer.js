import React, { Component } from 'react';
import Dot from './Dot';

const mapWidthInPixels = 1791;
const mapHeightInPixels = 1484;

class Container extends Component {
  state = {
    dots: [],
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
          const [xStr, yStr, color] = line.split(',');

          const x = parseFloat(xStr)*10.91;
          const y = parseFloat(yStr)*20.24;
          
          
          console.log(x, y)
          if (!isNaN(x) && !isNaN(y)) {
            return { x, y: mapHeightInPixels - y, color: color || 'red' }; // Default to red if color is not specified
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
          <Dot x={100} y={100} color="red" />
          {this.state.dots.map((dot, index) => (
            <Dot key={index} x={dot.x} y={dot.y} color={dot.color} />
          ))}
        </div>
      </div>
    );
  }
}

export default Container;

