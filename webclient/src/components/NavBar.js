import React, {useState} from 'react';
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';

function NavigationBar() {   

    const [fromRoom, setFromRoom] = useState('');
    const [toRoom, setToRoom] = useState('');

    const handleSelectFrom = (eventKey) => {
        setFromRoom(eventKey);
    };

    const handleSelectTo = (eventKey) => {
        setToRoom(eventKey);
    };

    const selectedRouteStyle = {
        fontSize: '20px', // Increase font size
        marginLeft: '20px', // Move a bit to the left
        fontFamily: 'Times New Roman, serif', // Change the font
        color: 'white', // Change the font color if needed
      };

    return (
        <Navbar bg="dark" variant="dark" expand="lg" >
            <Container>
                <Navbar.Brand href="#home" style={{ fontSize: '30px' }}>BearRoutes</Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="me-auto">
                        <Nav.Link href="#home">Home</Nav.Link>

                        <NavDropdown title="FROM" id = "dropdown-1" onSelect={handleSelectFrom}>
                            <NavDropdown.Item href = "Room 2-118">Room 2-118</NavDropdown.Item>
                            <NavDropdown.Item href = "#Room 2-001">Room 2-001</NavDropdown.Item>
                            <NavDropdown.Item href = "#Room 2-003">Room 2-003</NavDropdown.Item>
                            <NavDropdown.Item href = "#Room 2-049">Room 2-049</NavDropdown.Item>
                            <NavDropdown.Item href = "#Room 2-020">Room 2-020</NavDropdown.Item>
                        </NavDropdown>

                        <NavDropdown title="TO" id = "dropdown-2" onSelect={handleSelectTo}>
                            <NavDropdown.Item href = "Room 2-118">Room 2-118</NavDropdown.Item>
                            <NavDropdown.Item href = "#Room 2-001">Room 2-001</NavDropdown.Item>
                            <NavDropdown.Item href = "#Room 2-003">Room 2-003</NavDropdown.Item>
                            <NavDropdown.Item href = "#Room 2-049">Room 2-049</NavDropdown.Item>
                            <NavDropdown.Item href = "#Room 2-020">Room 2-020</NavDropdown.Item>
                        </NavDropdown>               

                        {/* Add more Nav.Link or NavDropdown components as needed */}
                    </Nav>
                    {/* Display the selected rooms */}
                    {fromRoom && toRoom && (
                        <Nav>
                            <Nav.Item>
                                <Nav.Link disabled style={selectedRouteStyle}>
                                Selected Route: From {fromRoom} To {toRoom}
                                </Nav.Link>
                            </Nav.Item>
                        </Nav>
                    )}
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}

export default NavigationBar;

