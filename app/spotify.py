import os
import spotipy
from sklearn.compose import ColumnTransformer
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from spotipy.oauth2 import SpotifyClientCredentials
from fastapi import APIRouter
import dotenv
import sys
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler, StandardScaler



dotenv.load_dotenv(dotenv.find_dotenv())
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')

router = APIRouter()
auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def song_to_artist(name):
    results = sp.search(q='track:' + name, type='track', limit=20)
    art = []
    long = len(results["tracks"]["items"][0]["artists"][0]["name"])
    for i in range(long):
        if results["tracks"]["items"][i]["artists"][0]["name"] not in art:
            art.append(results["tracks"]["items"][i]["artists"][0]["name"])
    return art

@router.get('/predict')
def song_suggester(artist, title):
    results = sp.search(q='artist:' + artist + ' track:' + title, type='track')
    trackId = results['tracks']['items'][0]['id']
    track_features = sp.audio_features(trackId)
    df = pd.DataFrame(track_features)
    df = df.drop(columns = ['loudness', "type","id","uri","track_href","analysis_url", "time_signature"])
    popularity =((sp.track(trackId))['popularity'])
    explicit = ((sp.track(trackId))['explicit'])
    df['popularity'] = popularity
    df['explicit'] = explicit
    df['id'] = trackId
    cols= ['id','acousticness','danceability', 'duration_ms','energy','instrumentalness','liveness', 'popularity','speechiness', 'tempo','valence','explicit','key','mode']
    df = df[cols]

    gi

    #df2_id = df['id']
    df2_features = df[df.columns[1:]]
    scalable_features = ['duration_ms', 'popularity', 'tempo', 'key']
    scaling_transformer = Pipeline (steps=[('scaler', StandardScaler ())])
    #knn = NearestNeighbors (n_neighbors=6)

    column_trans = ColumnTransformer (
        transformers=[
            ('scaled', scaling_transformer, scalable_features)],
        remainder='passthrough'
    )

    transformed_features2 = column_trans.fit_transform (df2_features)
    neighbors = model.kneighbors (transformed_features2[0].reshape (1, -1), return_distance=False)[0]
    df_song = pd.read_csv ('app/spotify_features_jjb.gz')['id']

    # for n in neighbors:
    # print(df_song.iloc[n])
    returned_songs = [df_song.iloc[n] for n in neighbors]

    track_names_list = []
    for x in returned_songs:
        track_names = ((sp.track(x))['name'])
        track_names_list.append(track_names)
    return (track_names_list)




#watchout for explicit(false or true) consider changing it to binary
#celine_df = (song_id('Celine Dion', 'my heart will go on'))

#print(celine_df)

#model = joblib.load('knnbaseline.joblib.gz')

#print((sp.track('33LC84JgLvK2KuW43MfaNq'))['popularity'])

#df2_id = celine_df['id']
#df2_features = celine_df[celine_df.columns[1:]]
#scalable_features = ['duration_ms', 'popularity', 'tempo', 'key']
#scaling_transformer = Pipeline(steps=[('scaler', StandardScaler())])
#knn = NearestNeighbors(n_neighbors=6)

#column_trans = ColumnTransformer(
    #transformers=[
         #('scaled', scaling_transformer, scalable_features)],
         #remainder='passthrough'
#)

#transformed_features2 = column_trans.fit_transform(df2_features)
#neighbors = model.kneighbors(transformed_features2[0].reshape(1,-1), return_distance=False)[0]
#df_song = pd.read_csv('spotify_features_jjb.gz')['id']

#for n in neighbors:
  #print(df_song.iloc[n])
#returned_songs = [df_song.iloc[n] for n in neighbors]
#print(returned_songs)


#celine_df = ((sp.track('2RM4jf1Xa9zPgMGRDiht8O'))['popularity'])

def song_features(artist, title):
    results = sp.search(q='artist:' + artist + ' track:' + title, type='track')
    trackId = results['tracks']['items'][0]['id']
    track_features = sp.audio_features(trackId)
    return track_features

