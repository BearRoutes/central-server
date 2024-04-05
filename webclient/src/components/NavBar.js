import React from 'react';
import { Navbar, Nav, Container, NavDropdown } from 'react-bootstrap';

function NavigationBar() {   

return (
    <Navbar bg="dark" variant="dark" expand="lg" >
        <Container>
            <Navbar.Brand href="#home" style={{ fontSize: '30px' }}>BearRoutes</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="me-auto">
                    <Nav.Link href="#home">Home</Nav.Link>

                    <NavDropdown title="FROM : address 1" id = "dropdown-1">
                        <NavDropdown.Item href = "#address 1">Room 1</NavDropdown.Item>
                        <NavDropdown.Item href = "#address 2">Room 2</NavDropdown.Item>
                        <NavDropdown.Item href = "#address 3">Room 3</NavDropdown.Item>
                        <NavDropdown.Item href = "#address 4">Room 4</NavDropdown.Item>
                        <NavDropdown.Item href = "#address 5">Room 5</NavDropdown.Item>
                        <NavDropdown.Item href = "#address 6">Room 6</NavDropdown.Item>
                    </NavDropdown>

                    <NavDropdown title="TO : address 2" id = "dropdown-1">
                        <NavDropdown.Item href = "#address 1">Room 1</NavDropdown.Item>
                        <NavDropdown.Item href = "#address 2">Room 2</NavDropdown.Item>
                        <NavDropdown.Item href = "#address 3">Room 3</NavDropdown.Item>
                        <NavDropdown.Item href = "#address 4">Room 4</NavDropdown.Item>
                        <NavDropdown.Item href = "#address 5">Room 5</NavDropdown.Item>
                        <NavDropdown.Item href = "#address 6">Room 6</NavDropdown.Item>
                    </NavDropdown>               

                    {/* Add more Nav.Link or NavDropdown components as needed */}
                </Nav>
            </Navbar.Collapse>
        </Container>
    </Navbar>
);
}

export default NavigationBar;

