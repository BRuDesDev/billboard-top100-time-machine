from bs4 import BeautifulSoup
import requests
import spotipy
import os

REDIRECT_URI = "https://example.com"
SCOPE = "playlist-modify-private"

# Get date from user input
date = input("What year would you like to travel to? Enter date in this format (YYYY-MM-DD): ")

# url to page with top 100 for week of date
url = "https://www.billboard.com/charts/hot-100/" + date

# Getting Soup
response = requests.get(url)
website = response.text
soup = BeautifulSoup(website, "html.parser")

songs = []
artists = []
# Scraping Song Names
song_names = soup.select("li ul li h3")
# Scraping Artist Names
artist_names = soup.find_all(name="span", class_="a-no-trucate")

# Add songs to list and get rid of tabs/newlines
for song in song_names:
    songs.append(song.text.replace("\n", "").replace("\t", ""))
# Add artists to list and get rid of tabs/newlines
for artist in artist_names:
    artists.append(artist.text.replace("\n", "").replace("\t", ""))

# Printing out Artist - Song
# for i in range(100):
#     print(f"{artists[i]} - {songs[i]}")

# Getting SpotifyOAuth object
oauth_object = spotipy.oauth2.SpotifyOAuth(client_id=os.environ['client_id'],
                                           client_secret=os.environ['client_secret'],
                                           redirect_uri=REDIRECT_URI,
                                           scope=SCOPE,
                                           show_dialog=True,
                                           cache_path="token.txt")

# Get Access Token
access_token = ""
token_info = oauth_object.get_cached_token()
if token_info:
    access_token = token_info["access_token"]

# Getting user id
sp = spotipy.Spotify(auth_manager=oauth_object)
user_id = sp.current_user()["id"]

# Authorize URL and get Redirect URL
authorize_url = oauth_object.get_authorize_url(state=None)

song_uris = []
year = date.split("-")[0]
# Create list of URI for each song
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Create private playlist to add songs to
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# Add songs to playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)