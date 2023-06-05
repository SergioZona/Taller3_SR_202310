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
                <Card.Img variant="top" src="https://d500.epimg.net/cincodias/imagenes/2020/12/31/lifestyle/1609408585_467254_1609408795_noticia_normal.jpg" />
                <Card.Body>
                    <Card.Title>{props.title}</Card.Title>
                    {props.percentage == "" ? <div> </div> : <Card.Text>
                        Probabilidad de que te guste <b>{props.percentage} </b>
                    </Card.Text>}
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