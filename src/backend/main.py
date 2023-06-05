"""Aditional libraries"""
import time
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from .recommendation_systems import model
from surprise import dump

"""Backend dependencies"""
import uvicorn
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from surprise import dump

# Create an instance of the FastAPI class
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get CSV
df_movies = pd.read_csv('backend/data/df_movies.csv')
df_movies.fillna("", inplace=True)

df_reviews = pd.read_csv('backend/data/df_ratings.csv')
df_reviews.fillna("", inplace=True)

df_links = pd.read_csv('backend/data/df_links.csv')
df_links.fillna("", inplace=True)

knn = dump.load('backend/data/knn.pkl')[1]

@app.get("/")
def root():
    return {"message": "Fast API in Python"}

"""------------------"""
"""ENDPOINTS - REVIEW"""
"""------------------"""
# Define a route to get all the rows from the database table

@app.get('/api/review')
async def get_review():
    data = df_reviews.to_dict(orient='records')
    return {'data': data}

"""------------------"""
"""ENDPOINTS - MOVIES"""
"""------------------"""

@app.get('/api/movie')
async def get_movie():
    data = df_movies.to_dict(orient='records')
    return {'data': data}

@app.get('/api/movie/{id}')
async def get_movie_by_id(id: str):  
    df_movies_id = df_movies.loc[df_movies['movieId'] == int(id)]
    data = df_movies_id.to_dict(orient='records')
    return {'data': data}

# Friends DataFrame
@app.get('/api/movie/recommendation/{user_id}/{movie_id}/{n}')
async def get_recommendations(user_id: int, movie_id: int, n: int):
    start_time = time.time()
    if len(df_reviews)>0:    
        print("Waiting for predictions...")

        top_n_movies = await model.get_top_n(user_id, movie_id, n, df_movies, df_reviews, df_links, knn)
        prediction = top_n_movies.to_dict(orient='records')
        print("--- %s seconds ---" % (time.time() - start_time))
        return {'data': prediction}    
    else:
        print("--- %s seconds ---" % (time.time() - start_time))
        return {'data': []}

"""------"""
""" MAIN """
"""------"""
# Run the app
if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
