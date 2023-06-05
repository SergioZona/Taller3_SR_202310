import React from 'react'
import "./cardPlaces.css"
import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';
import { useNavigate } from 'react-router-dom';


function CardPlaces(props) {
    const navigate = useNavigate();
    return (
        <div className="cardPlaces">
            {console.log(props)}
            <Card style={{ width: '18rem' }} onClick={props.onclickEnable ? () => navigate(`/${props.id}/${props.idPeli}/recomendaciones`) : null}>
                <Card.Img variant="top" src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Vue_de_nuit_de_la_Place_Stanislas_%C3%A0_Nancy.jpg" />
                <Card.Body>
                    <Card.Title>{props.title}</Card.Title>
                    <Card.Text>
                        Probabilidad de que te guste <b>{props.percentage} </b>
                    </Card.Text>
                </Card.Body>
                <ListGroup className="list-group-flush">
                    <ListGroup.Item> <b>Director: </b> {props.director}</ListGroup.Item>
                    <ListGroup.Item> <b>Actores:</b> {props.actors}</ListGroup.Item>
                    <ListGroup.Item> <b>Palabras clave: </b>{props.keywords} </ListGroup.Item>
                    <ListGroup.Item><b>La puedes ver en:</b> {props.watchProviders} </ListGroup.Item>

                </ListGroup>

                {/* <HoverRating /> */}

            </Card>

        </div>


    )
}

export default CardPlaces