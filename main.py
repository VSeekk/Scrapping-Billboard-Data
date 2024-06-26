CLIENT_ID ="YOUR CLIENT ID FROM SPOTIFY"
CLIENT_SECRET="CLIENT SECRET FROM SPOTIFY"
USER_NAME="YOUR USERNAME"
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#using  Beautiful soup to extract the list of top 100 songs in billboard on a particular date
from bs4 import BeautifulSoup
import requests

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

#API creation
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=USER_NAME,
    )
)

#creating URI links list for the billBored 100 songs
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


#creating a  playlist and adding songs to it
playlist = sp.user_playlist_create(user=USER_NAME, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
