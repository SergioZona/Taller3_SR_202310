import React, { useState } from 'react'
import { useParams } from 'react-router-dom';
import NavBar from '../navbar/navbar';
import { Col, Row } from 'react-bootstrap';
import CardPlaces from '../home/component/card/cardPlaces';

function Recomendation() {

    var movie =
    {
        "tmdbId": 640,
        "movieId": 5989,
        "title": "Catch me if you can (2002)",
        "actors": "Leo Dicaprio",
        "director": "Steven Spielberg",
        "keyWords": "fbi, con man, biography, based on true story",
        "similarMovies": "The longest Day, Clear and Present Danger",
        "watchProviders": "Max, HBO Max",
        "percentage": "98%"
    }
    const [data, setData] = useState([movie, movie, movie]);
    const { id } = useParams();
    const { nameMovie, setNameMovie } = useState("")
    const { idPelicula } = useParams();
    const URL = ""

    // useEffect(() => {
    //     fetch(URL)
    //         .then(response => response.json())
    //         .then(data => {
    //             setData(data.data);
    //         })
    //         .catch(error => console.error('Error:', error));
    // }, [data]);

    return (
        <div>
            <NavBar id={id} />
            <Row className="d-flex justify-content-between align-items-center encabezado">
                <Col>
                    <h1 className="text-center">Porque viste {nameMovie} te recomendamos ver: </h1>
                </Col>
            </Row>
            <Row className="body">
                {data.length > 0 ? (
                    data.map((item, index) => (
                        <Col key={index}>
                            <CardPlaces
                                title={item.title}
                                actors={item.actors}
                                director={item.director}
                                keywords={item.keyWords}
                                stars={item.stars}
                                percentage={item.percentage}
                                id={id}
                                idPeli={item.movieId}
                                watchProviders={item.watchProviders}
                                onclickEnable={false}
                            />
                        </Col>
                    ))
                ) : (
                    <div className='no-recomendations'>
                        Esperando . . .
                    </div>
                )}
            </Row>
        </div>
    );
}

export default Recomendation

