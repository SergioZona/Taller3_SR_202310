

import pandas as pd
import numpy as np
import re
from SPARQLWrapper import SPARQLWrapper, JSON
import ast
import random
seed = 2023
random.seed(seed)

import tmdbsimple as tmdb
tmdb.API_KEY = 'e41c8a68517883ed8a2d66aca50b3371'
tmdb.REQUESTS_TIMEOUT = 5  # seconds, for both connect and read

# Libraries
seed = 2023

def preprocess_movie_name(movie_name):
    # Remove parentheses and their contents using regular expressions
    processed_name = re.sub(r'\([^()]*\)', '', movie_name)
    
    # Remove leading/trailing whitespace
    processed_name = processed_name.strip()
    processed_name = processed_name.replace(' ','_')
    
    return processed_name

def replace_film(movies_list):
    movies = []
    remove = [" film", " (film)"]
    for movie in movies_list:  
        for i in remove:            
            movie = movie.replace(i,"").strip()
        movies.append(movie)    
    return movies

def get_movie_names_from_dbpedia(movie_uris):
    # Create a SPARQLWrapper instance and set the DBpedia endpoint URL
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    movies_names = []
    
    for i in range(0, len(movie_uris), 5):
        movies = movie_uris[i:i+5]
        # Compose the SPARQL query to retrieve the movie names
        query = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?movieName
        WHERE {
          VALUES ?movie {
            %s
          }
          ?movie rdfs:label ?movieName .
          FILTER (lang(?movieName) = 'en')
        }
        """ % ' '.join(['<'+uri+'>' for uri in movies])

        # Set the SPARQL query and request JSON results
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)

        # Execute the SPARQL query and retrieve the results
        results = sparql.query().convert()

        # Extract the movie names from the results
        movie_names_extract = [result['movieName']['value'] for result in results['results']['bindings']]
        movies_names.extend(movie_names_extract)
    return movies_names  

def get_movie_names_from_dbpedia(movie_uris):
    # Create a SPARQLWrapper instance and set the DBpedia endpoint URL
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
   
    # Compose the SPARQL query to retrieve the movie names
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?movieName
    WHERE {
      VALUES ?movie {
        %s
      }
      ?movie rdfs:label ?movieName .
      FILTER (lang(?movieName) = 'en')
    }
    """ % ' '.join(['<'+uri+'>' for uri in movie_uris])

    # Set the SPARQL query and request JSON results
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the SPARQL query and retrieve the results
    results = sparql.query().convert()

    # Extract the movie names from the results
    movies_names = [result['movieName']['value'] for result in results['results']['bindings']]
    return movies_names  

def get_similar_movies_by_starring(movie_title, actors_names):
    # Create a SPARQLWrapper instance and set the DBpedia endpoint URL
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    
    actors_names = [string.replace(" ", "_") for string in actors_names]
  
    # Compose the SPARQL query to retrieve similar movies based on shared actors
    query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT DISTINCT ?similarMovie
    WHERE {
      ?similarMovie dbo:starring ?actor .
      FILTER (?actor IN (%s))
      FILTER (?similarMovie != dbr:%s)
    }
    ORDER BY RAND()
    LIMIT 100
    """ % (", ".join(["dbr:" + actor_name for actor_name in actors_names]), movie_title)
    
    # Set the SPARQL query and request JSON results
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the SPARQL query and retrieve the results
    results = sparql.query().convert()

    # Extract the similar movie URIs from the results
    similar_movies = [result['similarMovie']['value'] for result in results['results']['bindings']]
    similar_movies = get_movie_names_from_dbpedia(similar_movies)
    return similar_movies

def get_similar_movies_by_director(movie_title, director_name):
    # Create a SPARQLWrapper instance and set the DBpedia endpoint URL
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    
    director_name = director_name.strip().replace(" ", "_")
     
    # Compose the SPARQL query to retrieve similar movies based on shared actors
    query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT DISTINCT ?similarMovie
    WHERE {
      ?similarMovie dbo:director ?director .
      FILTER (?director = dbr:%s)
      FILTER (?similarMovie != dbr:%s)
    }
    ORDER BY RAND()
    LIMIT 50
    """ % (director_name, movie_title)

    # Set the SPARQL query and request JSON results
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    # Execute the SPARQL query and retrieve the results
    results = sparql.query().convert()

    # Extract the similar movie URIs from the results
    similar_movies = [result['similarMovie']['value'] for result in results['results']['bindings']]
    similar_movies = get_movie_names_from_dbpedia(similar_movies)
    return similar_movies

# Iterate over the DataFrame and call the get_similar_movies function for each movie
def get_ontological_data(movie_title, director_name, actors_names):
    similar_movies_starring = get_similar_movies_by_starring(movie_title, actors_names)
    similar_movies_actors = get_similar_movies_by_director(movie_title, director_name)    
    similar_movies_starring.extend(similar_movies_actors)
    
    similar_movies = replace_film(list(set(similar_movies_starring)))
    
    # Create a DataFrame with a single column
    df = pd.DataFrame({'similar_movies': similar_movies})
    
    return df

def get_tmbd_id(movie):
    try:
        search = tmdb.Search()
        response = search.movie(query=movie)
        response_id = response["results"][0]['id']
        return response_id
    except:
        return np.nan    
    
def join_ontological_data(df_ontological, df_m_extended, df_l):    
    df_ontological['tmdbId'] = np.nan
    df_ontological['tmdbId'] = df_ontological['similar_movies'].apply(lambda x: get_tmbd_id(x))
    df_ontological['tmdbId'] = df_ontological['tmdbId'].fillna(0).astype(int)
    
    columns = ["tmdbId", "movieId", "title", "actors", "director", "keyWords", "similarMovies", "watchProviders"]

    df_merged = df_ontological.merge(df_l[['tmdbId', 'movieId']], on='tmdbId', how='left')
    df_merged = df_merged.dropna()
    df_merged = df_merged.merge(df_m_extended, on='movieId', how='left')
    df_merged = df_merged[columns]
    df_merged = df_merged.loc[df_merged['actors'].isna() == False]
    df_merged['movieId'] = df_merged['movieId'].astype(int)
    return df_merged
    
def knn_predict(user_id, item_id, knn):
    knn_prediction = knn.predict(user_id, item_id).est
    return knn_prediction

async def get_top_n(user_id, movie_id, n, df_m_extended, df, df_l, knn, sample = 1):   
    movie = df_m_extended.loc[df_m_extended['movieId'] == movie_id] # Movie that the users watches
    title = preprocess_movie_name(movie['title'].values[0])
    director = movie['director'].values[0]
    actors = [value.strip() for value in movie['actors'].values[0].split(',')]
       
    # Ontological filtering
    df_ontological = get_ontological_data(title, director, actors)
    df_final = join_ontological_data(df_ontological, df_m_extended, df_l)
    
    print("Data retrieved:", len(df_final))
    print()
    
    # Get all businesses the user has not reviewed
    all_items = set(df_final['movieId'].unique())
    reviewed_items = set(df.loc[df['userId'] == user_id]['movieId'].unique())
    unreviewed_items = all_items - reviewed_items
    
    print("Ontological filtered movies:", all_items)
    print()
    print("Reviewed:",reviewed_items)
    print()
    print("Unreviewed:", unreviewed_items)
    print()
    print("Total movies unreviewed:", len(unreviewed_items))
    print()
   
    unreviewed_items = list(unreviewed_items)
    num_items = len(unreviewed_items)
    num_sample = int(num_items * sample)
    unreviewed_items = random.sample(unreviewed_items, num_sample)
    
    print("Predicting movies...")
    
    # Make predictions for unreviewed businesses and sort by prediction
    predictions = []
    for item_id in unreviewed_items:
        prediction = knn_predict(user_id, item_id, knn)
        predictions.append((item_id, prediction))
        #print((business_id, prediction))
    predictions.sort(key=lambda x: x[1], reverse=True)
    
    print("Retrieving data from DBPedia...")
    print()
    
    print("User:", user_id)
    print()
    print("Movie title:", movie['title'].values[0])
    print("Director:", director)
    print("Actors:", actors)
    print()

    # Get top n recommended businesses and their predictions
    top_n = predictions[:n]
    top_n_items = [x[0] for x in top_n]
    top_n_predictions = [x[1] for x in top_n]
    top_n_percentage = [str(round(x/5*100, 2))+"%" for x in top_n_predictions]

    # Create DataFrame with business ids and predictions
    columns = ["tmdbId", "movieId", "title", "actors", "director", "keyWords", "similarMovies", "watchProviders"]

    df_top_n = pd.DataFrame({'movieId': top_n_items, 'prediction': top_n_predictions, 'percentage': top_n_percentage})
    df_top_n =  pd.merge(df_top_n, df_final, on='movieId')
    return df_top_n

