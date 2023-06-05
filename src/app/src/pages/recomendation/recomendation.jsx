import React, { useState } from 'react'
import { useParams } from 'react-router-dom';
import NavBar from '../navbar/navbar';
import { Col, Row } from 'react-bootstrap';
import CardPlaces from '../home/component/card/cardPlaces';

function Recomendation() {


    const movies =

        [
            {
                "movieId": 176371,
                "prediction": 46254666374843200,
                "percentage": "92.51%",
                "tmdbId": 335984,
                "title": "Blade Runner 2049 (2017)",
                "actors": "Ryan Gosling, Harrison Ford, Ana de Armas, Sylvia Hoeks, Robin Wright",
                "director": "Denis Villeneuve", "keyWords": "artificial intelligence, bounty hunter, android, future, dystopia", "similarMovies": "Young Guns II, S.W.A.T., High School High, Nineteen Eighty-Four, The Last Boy Scout", "watchProviders": "Hulu"
            },
            { "movieId": 3111, "prediction": 450572811867691, "percentage": "90.11%", "tmdbId": 13681, "title": "Places in the Heart (1984)", "actors": "Sally Field, Lindsay Crouse, John Malkovich, Danny Glover, Ed Harris", "director": "Robert Benton", "keyWords": "ku klux klan, loss of loved one, war veteran, texas, kidnapping", "similarMovies": "Ace Ventura: When Nature Calls, Thesis, Flightplan, Transporter 2, Kiss the Girls", "watchProviders": "fuboTV" },
            { "movieId": 107630, "prediction": 4.5, "percentage": "90.0%", "tmdbId": 27584, "title": "High School (2010)", "actors": "Adrien Brody, Matt Bush, Sean Marquette, Colin Hanks, Michael Chiklis", "director": "John Stalberg Jr.", "keyWords": "university, drugs, aftercreditsstinger", "similarMovies": "The Faculty, Ferris Bueller's Day Off, Belushi's Toilet, Woodstock, DodgeBall: A True Underdog Story", "watchProviders": "Amazon Prime Video" },
            { "movieId": 86781, "prediction": 4378048907260690, "percentage": "87.56%", "tmdbId": 46738, "title": "Incendies (2010)", "actors": "Lubna Azabal, MÃ©lissa DÃ©sormeaux-Poulin, Maxim Gaudette, RÃ©my Girard, Allen Altman", "director": "Denis Villeneuve", "keyWords": "prison, middle east, rape, muslim, militia", "similarMovies": "Just Cause, Young Guns II, The Longest Yard, The Man in the Iron Mask, The Last Boy Scout", "watchProviders": "" },
            { "movieId": 165101, "prediction": 4327880932253130, "percentage": "86.56%", "tmdbId": 207932, "title": "Inferno (2016)", "actors": "Tom Hanks, Felicity Jones, Omar Sy, Irrfan Khan, Sidse Babett Knudsen", "director": "Ron Howard", "keyWords": "italy, based on novel or book, europe, amnesia, sequel", "similarMovies": "Tristan & Isolde, Police Story, Only You, Just Cause, Love Story", "watchProviders": "Starz Apple TV Channel, AMC Plus Apple TV Channel , Starz Roku Premium Channel, Starz, DIRECTV, Starz Amazon Channel" },
            { "movieId": 164179, "prediction": 4320304710091570, "percentage": "86.41%", "tmdbId": 329865, "title": "Arrival (2016)", "actors": "Amy Adams, Jeremy Renner, Forest Whitaker, Michael Stuhlbarg, Tzi Ma", "director": "Denis Villeneuve", "keyWords": "spacecraft, time, language, loss, alien", "similarMovies": "The Four Feathers, Broken Arrow, The Faculty, The Avengers, The Core", "watchProviders": "Amazon Prime Video, fuboTV, Paramount Plus, Paramount Plus Apple TV Channel , Paramount+ Amazon Channel, MGM Plus Amazon Channel, Paramount+ Roku Premium Channel, MGM Plus Roku Premium Channel, MGM Plus" },
            { "movieId": 609, "prediction": 4248675472325340, "percentage": "84.97%", "tmdbId": 25059, "title": "Homeward Bound II: Lost in San Francisco (1996)", "actors": "Michael J. Fox, Sally Field, Ralph Waite, Robert Hays, Kim Greist", "director": "David R. Ellis", "keyWords": "pets", "similarMovies": "Ace Ventura: When Nature Calls, Lassie Come Home, Pet Sematary, Garfield, Spirit: Stallion of the Cimarron", "watchProviders": "Disney Plus" },
            { "movieId": 2797, "prediction": 416334317236373, "percentage": "83.27%", "tmdbId": 2280, "title": "Big (1988)", "actors": "Tom Hanks, Elizabeth Perkins, Robert Loggia, John Heard, Jared Rushton", "director": "Penny Marshall", "keyWords": "baseball, co-workers relationship, body-swap, magic realism, bronx, new york city", "similarMovies": "The Brady Bunch Movie, To Wong Foo, Thanks for Everything! Julie Newmar, John Tucker Must Die, Microcosmos, Look Who's Talking Too", "watchProviders": "Disney Plus, AMC Plus Apple TV Channel " },
            { "movieId": 56788, "prediction": 4097065519457290, "percentage": "81.94%", "tmdbId": 6538, "title": "Charlie Wilson's War (2007)", "actors": "Tom Hanks, Amy Adams, Julia Roberts, Philip Seymour Hoffman, Emily Blunt", "director": "Mike Nichols", "keyWords": "cairo, washington dc, usa, alcohol, cia, helicopter", "similarMovies": "The Element of Crime, Spies Like Us, Broken Arrow, 11:14, Clear and Present Danger", "watchProviders": "Netflix, Netflix basic with Ads" },
            { "movieId": 500, "prediction": 408194559390603, "percentage": "81.64%", "tmdbId": 788, "title": "Mrs. Doubtfire (1993)", "actors": "Robin Williams, Sally Field, Pierce Brosnan, Lisa Jakub, Matthew Lawrence", "director": "Chris Columbus", "keyWords": "san francisco, california, transvestite, parent child relationship, restaurant, nanny", "similarMovies": "The Man, The Good Son, The Man in the Iron Mask, Thir13en Ghosts, Glass Chin", "watchProviders": "Starz Apple TV Channel, Starz, DIRECTV, Starz Amazon Channel" }
        ]

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
    const [data, setData] = useState(movies);
    const { id } = useParams();
    const { nameMovie, setNameMovie } = useState("Big (1988)")
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
                    <h1 className="text-center" style={{ color: "white" }}>Porque viste Big (1988), te recomendamos ver: </h1>
                </Col>
            </Row>
            <Row className="body">
                {data.length > 0 ? (
                    data.map((item, index) => (
                        <Col key={index}>
                            {console.log(item)}
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

