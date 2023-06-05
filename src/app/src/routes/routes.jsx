import { Route, Routes } from "react-router-dom";
import React from 'react';
import Home from "../pages/home/home";
import Login from "../pages/login/login";
import Recomendation from "../pages/recomendation/recomendation";

const CreateRoutes = () => (
    <Routes>
        <Route exact path="/" element={<Login />} />
        <Route exact path="/:id/peliculas" element={<Home />} />
        <Route exact path="/:id/:idPelicula/recomendaciones" element={<Recomendation />} />
    </Routes>
);

export default CreateRoutes;