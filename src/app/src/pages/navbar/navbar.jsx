import React from 'react'
import { Container, Nav, Navbar, Button, Form } from 'react-bootstrap'
import { Link, useNavigate } from 'react-router-dom';
import "./navbar.css"

function NavBar(props) {
    const id = props.id;
    const navigate = useNavigate();
    return (
        <div >
            <Navbar expand="lg">
                <Container fluid>
                    <Navbar.Brand href={`/${id}/peliculas`} style={{ color: "white" }}>Menu</Navbar.Brand>
                    <Navbar.Toggle aria-controls="navbarScroll" />
                    <Navbar.Collapse id="navbarScroll">
                        <Nav
                            className="me-auto my-2 my-lg-0"
                            style={{ maxHeight: '100px' }}
                            navbarScroll
                        >
                            <Nav.Link style={{ color: "white" }} onClick={() => navigate(`/${id}/peliculas`)}>Películas</Nav.Link>
                            {/* <Nav.Link onClick={() => navigate(`/${id}/recomendaciones`)}>Mis recomendaciones</Nav.Link> */}
                        </Nav>
                        <Form className="d-flex form">
                            <Form.Control
                                type="search"
                                placeholder="Search"
                                className="me-2"
                                aria-label="Search"
                            />
                            <Button variant="success">Search</Button>

                        </Form>
                        <Link to="/" className="custom-btn btn-10" > Log out</Link>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
            <hr />
        </div >

    );
}
export default NavBar