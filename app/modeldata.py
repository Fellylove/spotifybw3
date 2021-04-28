import pandas as pd

test_data = pd.read_csv (
    'https://raw.githubusercontent.com/Build-Week-Spotify-Song-Suggester-1/Data-science/master/SpotifyAudioFeaturesApril2019.csv')
test_data = test_data.drop(columns = ["valence", "tempo",
                            "duration_ms", "time_signature"])
#print(test_data.head(2))
list1 = ['2RM4jf1Xa9zPgMGRDiht8O','1tHDG53xJNGsItRA3vfVgs','3J2Jpw61sO7l6Hc7qdYV91']
mask = test_data['track_id'].isin(list1)
df2 = test_data.loc[~mask]

for i in list1:
    d3 = test_data.loc[test_data['track_id'] == i, "artist_name"]
    list_songs = d3.to_list()

    print(list_songs)