import React from 'react';
import { Link } from 'react-router-dom';
import { Navbar, Nav, NavDropdown, Button, Form, FormControl } from 'react-bootstrap';

const Navigation = () => {



    return (
        <Navbar expand="md" bg="primary" variant="dark">
            <Link className="navbar-brand" to="/">Vagabond</Link>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <Link className="nav-item nav-link" to="/">Home</Link>
                    <Link className="nav-item nav-link" to="/about">About</Link>
                    <Link className="nav-item nav-link" to="/test">Log in</Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );

}

export default Navigation;