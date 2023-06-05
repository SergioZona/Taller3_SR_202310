"""Aditional libraries"""
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
from .recommendation_systems import model
from surprise import dump

"""Backend dependencies"""
import sqlite3
import uvicorn
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import hashlib
from datetime import datetime


# Issue corrected: https://stackoverflow.com/questions/65635346/how-can-i-enable-cors-in-fastapi
# Create an instance of the FastAPI class
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to the SQLite3 database
# conn = sqlite3.connect('../data/data.db') # Si ejecuto el script desde SRC.
conn = sqlite3.connect('data/data.db')

@app.get("/")
def root():
    return {"message": "Fast API in Python"}

"""----------------"""
"""ENDPOINTS - USER"""
"""----------------"""

# Define a route to get all the rows from the database table

@app.get('/api/user')
async def get_user():
    # Create a cursor object
    cur = conn.cursor()

    # Execute a SELECT statement to get all the rows from the table
    cur.execute('SELECT * FROM user')

    # Fetch all the rows and convert them to a list of dictionaries
    rows = cur.fetchall()

    data = [{'user_id': row[0],
             'name': row[1],
             'review_count': row[2],
             'yelping_since': row[3],
             'friends': row[4],
             'average_stars': row[5]
             } for row in rows]

    # Close the cursor
    cur.close()

    # Return the data as a JSON response
    return {'data': data}

# Define a route to get a single row from the database table by id


@app.get('/api/user/{id}')
async def get_user_by_id(id: str):
    # Create a cursor object
    cur = conn.cursor()

    # Execute a SELECT statement to get the row with the specified id
    cur.execute('SELECT * FROM user WHERE user_id = ?', (id,))

    # Fetch the row and convert it to a dictionary
    row = cur.fetchone()
    data = {'user_id': row[0],
             'name': row[1],
             'review_count': row[2],
             'yelping_since': row[3],
             'friends': row[4],
             'average_stars': row[5]
            }
    # Close the cursor
    cur.close()
    # Return the data as a JSON response
    return {'data': data}


@app.post("/api/user")
async def create_user(username: str = Body(...), gender: str = Body(...), age: str = Body(...), country: str = Body(...), password: str = Body(...)):
    print("Creating user...")
    newPassword = password
    password_hash = hashlib.sha256(
        bytes(newPassword, encoding='utf-8')).hexdigest()

    # Create a cursor object
    cur = conn.cursor()

    cur.execute('INSERT INTO user (user_id, gender, age, country, registered, password_hash) VALUES (?, ?, ?, ?, ?, ?)',
                (username, gender, age, country, datetime.now(), password_hash))
    conn.commit()
    cur.close()
    return {"message": "User created successfully!"}


@app.post("/api/user/login")
async def login(username: str = Body(...), password: str = Body(...)):
    data = await get_user_by_id(username)
    data = data["data"]
    newPassword = password
    password_hash = hashlib.sha256(
        bytes(newPassword, encoding='utf-8')).hexdigest()
    if (password_hash == data["password_hash"]):     
        return {"message": "LogIn successfully!"}
    return {"message": "Password or account invalid"}


"""------------------"""
"""ENDPOINTS - REVIEW"""
"""------------------"""
# Define a route to get all the rows from the database table

@app.get('/api/review')
async def get_review():
    # Create a cursor object
    cur = conn.cursor()

    # Execute a SELECT statement to get all the rows from the table
    cur.execute('SELECT * FROM review')

    # Fetch all the rows and convert them to a list of dictionaries
    rows = cur.fetchall()
    data = [{'review_id': row[0],
             'user_id': row[1],
             'business_id': row[2],
             'stars': row[3],
             'text': row[4],
             'date': row[5]
             } for row in rows]

    # Close the cursor
    cur.close()

    # Return the data as a JSON response
    return {'data': data}

"""--------------------"""
"""ENDPOINTS - BUSINESS"""
"""--------------------"""

@app.get('/api/business')
async def get_business():
    # Create a cursor object
    cur = conn.cursor()

    # Execute a SELECT statement to get all the rows from the table
    cur.execute('SELECT * FROM business')

    # Fetch all the rows and convert them to a list of dictionaries
    rows = cur.fetchall()
    data = [{'business_id': row[0],
             'name': row[1],
             'address': row[2],
             'city': row[3],
             'stars': row[4],
             'review_count': row[5],
             'categories': row[6]
             } for row in rows]

    # Close the cursor
    cur.close()

    # Return the data as a JSON response
    return {'data': data}

@app.get('/api/business/{id}')
async def get_business_by_id(id: str):
    # Create a cursor object
    cur = conn.cursor()

    # Execute a SELECT statement to get the row with the specified id
    cur.execute('SELECT * FROM business WHERE business_id = ?', (id,))

    # Fetch the row and convert it to a dictionary
    row = cur.fetchone()
    data = {'business_id': row[0],
             'name': row[1],
             'address': row[2],
             'city': row[3],
             'stars': row[4],
             'review_count': row[5],
             'categories': row[6]
            }
    # Close the cursor
    cur.close()
    # Return the data as a JSON response
    return {'data': data}


# Friends DataFrame
@app.get('/api/business/recommendation/{user_id}/{top_business}')
async def get_recommendations(user_id: str, top_business: int):
    df_business = await get_business()
    df_business = df_business["data"]
    df_business = pd.DataFrame(df_business)

    df_review = await get_review()
    df_review = df_review["data"]
    df_review = pd.DataFrame(df_review)
    df = df_review[['user_id', 'business_id', 'stars']]

    svd = dump.load('data/models/svd.pkl')[1]
    knn = dump.load('data/models/knn.pkl')[1]

    df_user = await get_user()
    df_user = df_user["data"]
    df_user = pd.DataFrame(df_user)

    df_user_friends = df_user.copy()
    df_user_friends['friends'] = df_user_friends['friends'].str.split(', ')

    if len(df_review)>0:    
        print("Waiting for predictions...")
        prediction = await model.get_top_n(svd, knn, df, df_user_friends, df_business, df_review, user_id, top_business)
        prediction = prediction.to_dict(orient='records')
        return {'data': prediction}    
    else:
        return {'data': []}

"""------"""
""" MAIN """
"""------"""
# Run the app
if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
