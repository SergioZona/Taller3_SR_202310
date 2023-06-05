import React from 'react'
import CardPlaces from './component/card/cardPlaces'
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import "./home.css"
import { useParams } from 'react-router-dom';
import NavBar from '../navbar/navbar';
import { useState, useEffect } from 'react';

function Home(props) {
    const movies =

        [
            { "movieId": 609, "prediction": 4248675472325340, "percentage": "84.97%", "tmdbId": 25059, "title": "Homeward Bound II: Lost in San Francisco (1996)", "actors": "Michael J. Fox, Sally Field, Ralph Waite, Robert Hays, Kim Greist", "director": "David R. Ellis", "keyWords": "pets", "similarMovies": "Ace Ventura: When Nature Calls, Lassie Come Home, Pet Sematary, Garfield, Spirit: Stallion of the Cimarron", "watchProviders": "Disney Plus" },
            { "movieId": 2797, "prediction": 416334317236373, "percentage": "83.27%", "tmdbId": 2280, "title": "Big (1988)", "actors": "Tom Hanks, Elizabeth Perkins, Robert Loggia, John Heard, Jared Rushton", "director": "Penny Marshall", "keyWords": "baseball, co-workers relationship, body-swap, magic realism, bronx, new york city", "similarMovies": "The Brady Bunch Movie, To Wong Foo, Thanks for Everything! Julie Newmar, John Tucker Must Die, Microcosmos, Look Who's Talking Too", "watchProviders": "Disney Plus, AMC Plus Apple TV Channel " },
            { "movieId": 56788, "prediction": 4097065519457290, "percentage": "81.94%", "tmdbId": 6538, "title": "Charlie Wilson's War (2007)", "actors": "Tom Hanks, Amy Adams, Julia Roberts, Philip Seymour Hoffman, Emily Blunt", "director": "Mike Nichols", "keyWords": "cairo, washington dc, usa, alcohol, cia, helicopter", "similarMovies": "The Element of Crime, Spies Like Us, Broken Arrow, 11:14, Clear and Present Danger", "watchProviders": "Netflix, Netflix basic with Ads" },
            { "movieId": 500, "prediction": 408194559390603, "percentage": "81.64%", "tmdbId": 788, "title": "Mrs. Doubtfire (1993)", "actors": "Robin Williams, Sally Field, Pierce Brosnan, Lisa Jakub, Matthew Lawrence", "director": "Chris Columbus", "keyWords": "san francisco, california, transvestite, parent child relationship, restaurant, nanny", "similarMovies": "The Man, The Good Son, The Man in the Iron Mask, Thir13en Ghosts, Glass Chin", "watchProviders": "Starz Apple TV Channel, Starz, DIRECTV, Starz Amazon Channel" },
            { "movieId": 164179, "prediction": 4320304710091570, "percentage": "86.41%", "tmdbId": 329865, "title": "Arrival (2016)", "actors": "Amy Adams, Jeremy Renner, Forest Whitaker, Michael Stuhlbarg, Tzi Ma", "director": "Denis Villeneuve", "keyWords": "spacecraft, time, language, loss, alien", "similarMovies": "The Four Feathers, Broken Arrow, The Faculty, The Avengers, The Core", "watchProviders": "Amazon Prime Video, fuboTV, Paramount Plus, Paramount Plus Apple TV Channel , Paramount+ Amazon Channel, MGM Plus Amazon Channel, Paramount+ Roku Premium Channel, MGM Plus Roku Premium Channel, MGM Plus" }
        ]

    const [data, setData] = useState(movies);
    const { id } = useParams();
    const URL = "";

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
                    <h1 className="text-center" style={{ color: "White" }}>Películas</h1>
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
                                percentage={""}
                                id={id}
                                idPeli={item.movieId}
                                watchProviders={item.watchProviders}
                                onclickEnable={true}
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

export default Home