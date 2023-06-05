import React from 'react'
import HoverRating from '../raiting/hoverRaiting'
import "./calificaciones.css"
function Calificaciones() {
    return (
        <div className='calificacion'><HoverRating />
            <form >
                <textarea rows="4" cols="60" type="text" name="comentario" placeholder="Comentario" onChange={(e) => { }} ></textarea>
            </form></div>
    )
}

export default Calificaciones