# Libraries
seed = 2023
import random
import pandas as pd
import numpy as np

from surprise import KNNWithZScore, Dataset, Reader
from surprise.model_selection import train_test_split

from surprise import Dataset, Reader, KNNWithZScore
from surprise.model_selection import train_test_split


def get_business_city(df_business, df_review_f, business_id, should_print = False):
    try:
        city = df_business[df_business["business_id"] == business_id]["city"].tolist()[0]
        business_in_city = df_business[df_business["city"] == city]["business_id"].tolist()
        df_city = df_review_f[df_review_f['business_id'].isin(business_in_city)]
        df_city = df_city[["user_id","business_id", "stars"]]
        
        if should_print:
            print(city)
            print("Num. reviews", df_city.shape[0])
            print("-------------------")
        return df_city
    except:
        return pd.DataFrame()

def get_knn_city(df_business, df_review_f, user_id, business_id, should_print = False):
    df_city = get_business_city(df_business, df_review_f, business_id, should_print)
    
    try:
        # Load data 
        if df_city.shape[0] >= 5:
            reader = Reader(rating_scale=(1, 5))
            data = Dataset.load_from_df(df_city, reader)

            # Split data
            trainset, testset = train_test_split(data, test_size=0.2, random_state=seed)

            knn = KNNWithZScore(k = 2, sim_options={'name': 'pearson', 'user_based':True}, random_state=seed, verbose=False)
            knn.fit(trainset)
            
            return knn
        else: 
            return None
    except:
        return None
    
def get_user_friends(df, df_user_friends, user_id, should_print = False):
    friends_set = df_user_friends[df_user_friends['user_id'] == user_id]
    if friends_set.shape[0] == 0:
        return pd.DataFrame()
    else:
        friends_set = friends_set["friends"].tolist()[0]
        friends_set = set(friends_set)

        df_friends = df.copy()
        df_friends = df_friends[df_friends['user_id'].isin(friends_set)]
        
        if should_print:
            print("Friends information")
            print(df_friends.describe())
            print("-------------------")
        return df_friends

def get_knn_friends(df, df_user_friends, user_id, business_id, should_print = False):
    df_friends = get_user_friends(df, df_user_friends, user_id, should_print)  
    
    try:
        # Load data 
        if df_friends.shape[0] >= 5:
            reader = Reader(rating_scale=(1, 5))
            data = Dataset.load_from_df(df_friends, reader)

            # Split data
            trainset, testset = train_test_split(data, test_size=0.2, random_state=seed)

            knn = KNNWithZScore(k = 2, sim_options={'name': 'pearson', 'user_based':True}, random_state=seed, verbose=False)
            knn.fit(trainset)
            
            return knn
        else: 
            return None
    except:
        return None

def get_weights(city_successful, friends_successful):
    # Order: SVD, KNN, KNN_City, KNN_Friends
    # 4 Cases according to the booleans
    
    if city_successful and friends_successful:
        return [0.25, 0.5, 0.2, 0.05]
    elif city_successful and not friends_successful:
        return [0.3, 0.5, 0.2, 0.0]
    elif not city_successful and friends_successful:
        return [0.3, 0.6, 0.0, 0.1]
    else:
        return [0.4, 0.6, 0.0, 0.0]

# Make hybrid predictions
def hybrid_predict(svd, knn, df, df_user_friends, df_business, df_review_f, user_id, business_id, should_print = False):
    knn_city = get_knn_city(df_business, df_review_f, user_id, business_id, should_print) 
    knn_friends = get_knn_friends(df, df_user_friends, user_id, business_id, should_print)
    city_successful = knn_city is not None
    friends_successful = knn_friends is not None
    
    svd_prediction = svd.predict(user_id, business_id).est
    knn_prediction = knn.predict(user_id, business_id).est
    knn_city_prediction = 0
    knn_friends_prediction = 0

    if city_successful:
        knn_city_prediction = knn_city.predict(user_id, business_id).est

    if friends_successful:
        knn_friends_prediction = knn_friends.predict(user_id, business_id).est

    if should_print:
        print("SVD:", svd_prediction)
        print("KNN:", knn_prediction)
        print("KNN City:", "There is not enough information to create a recommendation model." if not city_successful else knn_city_prediction)
        print("KNN Friends:", "There is not enough information to create a recommendation model." if not friends_successful else knn_friends_prediction)
        print("-------------------")
    
    models_predictions = [svd_prediction, knn_prediction, knn_city_prediction, knn_friends_prediction]
    weights = get_weights(city_successful, friends_successful)
    
    hybrid_prediction = np.dot(weights, models_predictions)
    
    return hybrid_prediction

async def get_top_n(svd, knn, df, df_user_friends, df_business, df_review_f, user_id, n):
    print("User:", user_id)
    
    # Get all businesses the user has not reviewed
    all_businesses = set(df['business_id'].unique())
    reviewed_businesses = set(df[df['user_id'] == user_id]['business_id'].unique())
    unreviewed_businesses = all_businesses - reviewed_businesses
    print("Total business:", len(unreviewed_businesses))
    
    unreviewed_businesses = list(unreviewed_businesses)
    num_business = len(unreviewed_businesses)
    num_sample = int(num_business * 0.01)
    unreviewed_businesses = random.sample(unreviewed_businesses, num_sample)
    
    # Make predictions for unreviewed businesses and sort by prediction
    predictions = []
    for business_id in unreviewed_businesses:
        prediction = hybrid_predict(svd, knn, df, df_user_friends, df_business, df_review_f, user_id, business_id, False)
        predictions.append((business_id, prediction))
        #print((business_id, prediction))
    predictions.sort(key=lambda x: x[1], reverse=True)

    # Get top n recommended businesses and their predictions
    top_n = predictions[:n]
    top_n_businesses = [x[0] for x in top_n]
    top_n_predictions = [x[1] for x in top_n]
    top_n_percentage = [str(round(x/5*100, 2))+"%" for x in top_n_predictions]

    # Create DataFrame with business ids and predictions
    df_top_n = pd.DataFrame({'business_id': top_n_businesses, 'prediction': top_n_predictions, 'percentage': top_n_percentage})
    df_top_n =  pd.merge(df_top_n, df_business, on='business_id')
    return df_top_n
