from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
date = input("What year do you want to travel to?\n (YYYY-MM-DD format)")

url = f"https://www.billboard.com/charts/hot-100/{date}/"

year = date.split("-")[0]

response = requests.get(url)

html_contents = response.content


soup = BeautifulSoup(html_contents, "html.parser")

titles = soup.select("li ul li h3")


song_names = [title.get_text().strip() for title in titles]

spotify_client_id = "f74a1102d6a9408c83c41d700fec6d67"
spotify_client_secret = "022c045fada4439e91b4db3ed923379b"
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'
my_redirect_uri = "http://example.com"


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="Ryu Suzuki",
    )
)

song_uris = []
user_id = sp.current_user()['id']
for song in song_names:
    result = sp.search(q=f"track:{song}, year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        time.sleep(10)
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} playlist", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

