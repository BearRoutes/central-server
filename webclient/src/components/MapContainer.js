import React, { Component } from 'react';
import Dot from './Dot';

const mapWidthInPixels = 1791;
const mapHeightInPixels = 984;

class Container extends Component {
  constructor(props) {
    super(props);
    this.state = {
      dots: [],
    };
    // Binding this context to methods
    this.addDot = this.addDot.bind(this);
    this.handleWheel = this.handleWheel.bind(this);
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

  handleWheel(e) {
    e.preventDefault();
    const zoomLevel = this.props.zoomLevel;
    const setZoomLevel = this.props.setZoomLevel;
    const newZoomLevel = e.deltaY < 0 ? Math.min(zoomLevel + 0.1, 3) : Math.max(zoomLevel - 0.1, 0.5);
    setZoomLevel(newZoomLevel);
  }

  addDot(x, y, color = 'red') {
    const newDot = { x, y, color };
    this.setState(prevState => ({
      dots: [...prevState.dots, newDot],
    }));
  }

  render() {
    const { zoomLevel, dots } = this.props;
    return (
        <div className="floor-map-container" style={{ width: `${mapWidthInPixels}px`, height: `${mapHeightInPixels}px`, position: 'relative' }}>
          {dots.map((dot, index) => (
            <Dot key={index} x={dot.x} y={dot.y} zoom={zoomLevel} color={dot.color} />
          ))}
        </div>
      );
  }
}

export default Container;
