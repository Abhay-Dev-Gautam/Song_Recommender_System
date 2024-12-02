import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Function to initialize Spotify client
def initialize_spotify_client(client_id, client_secret):
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name, sp):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song, sp):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist, sp))
        recommended_music_names.append(music.iloc[i[0]].song)
    return recommended_music_names, recommended_music_posters

# Streamlit App
st.header('Music Recommender System')

# Spotify API credentials input
st.subheader("Enter your Spotify API credentials")
client_id = st.text_input("Spotify Client ID", type="password")
client_secret = st.text_input("Spotify Client Secret", type="password")

if client_id and client_secret:
    # Initialize Spotify client
    sp = initialize_spotify_client(client_id, client_secret)

    # Load data
    music = pickle.load(open(r"C:\Users\Abhay\Documents\Project\df.pkl", 'rb'))
    similarity = pickle.load(open(r"C:\Users\Abhay\Documents\Project\similarity.pkl", 'rb'))

    # Song recommendation section
    music_list = music['song'].values
    selected_song = st.selectbox("Type or select a song from the dropdown", music_list)

    if st.button('Show Recommendation'):
        recommended_music_names, recommended_music_posters = recommend(selected_song, sp)
        cols = st.columns(5)
        for i, col in enumerate(cols):
            col.text(recommended_music_names[i])
            col.image(recommended_music_posters[i])

else:
    st.warning("Please enter your Spotify API credentials to proceed.")
