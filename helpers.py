import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util

from json.decoder import JSONDecodeError
# User ID = 129206905

username = sys.argv[1]
scope = 'playlist-read-private'
client_id = 'f894c2bd3ea34b8d8e3942df44008f2b'
client_secret = 'a307ed1d74a5453293469170e49f1c3d'
redirect_uri = 'https://google.com.sg/'

try:
    token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()

# Returns the top [length] number of songs that satisfy the 5 given criteria
def suggest(genre, year, length, acoustic, dance, energy, valence, Acoustic, Dance, Energy, Valence):
    # acoustic/dance are lower bounds. Acoustic/Dance are upper bounds
    genre = genre
    dance = dance
    year = year
    acoustic = acoustic
    N = 50
    i = 0
    recommend_names = []
    recommend_artist = []
    track_IDs = []
    while len(recommend_names) < length:
        # Saves all songs IDs that fall within genre and year given
        searchQuery = spotifyObject.search(q='genre:' + genre + ' year:' + year, limit=N, offset=i, market='SG')
        for j in range(N):
            track_id = searchQuery['tracks']['items'][j]['id']
            track_IDs.append(track_id)

        # Of the songs suggested, save the names and artists of those that pass the given criteria
        for id in track_IDs[i:i+N]:
            result = check(id, acoustic, dance, energy, valence, Acoustic, Dance, Energy, Valence)
            if result != None:
                artist = spotifyObject.track(id)
                artist_name = artist['artists'][0]['name']
                recommend_artist.append(artist_name)
                recommend_names.append(result)

# Returns a list of names of all the songs that passed the criteria
        i += N
    return (recommend_names[:length], recommend_artist[:length])


def check(id, acoustic, dance, energy, valence, Acoustic, Dance, Energy, Valence):
    satisfyLower = False
    satisfyUpper = False

    # Pulls out song features of each track
    track_features = spotifyObject.audio_features(tracks=id)
    track_acoustic = track_features[0]['acousticness']
    track_dance = track_features[0]['danceability']
    track_energy = track_features[0]['energy']
    track_valence = track_features[0]['valence']

    name = spotifyObject.track(id)
    track_name = name['name']

    # If the features of the track pass the given criteria, return the track name
    if (track_acoustic < Acoustic
        and  track_dance < Dance
        and track_energy < Energy
        and track_valence < Valence):
        satisfyUpper = True

    if (track_acoustic > acoustic
        and track_dance > dance
        and track_energy > energy
        and track_valence > valence):
        satisfyLower = True


    if satisfyLower and satisfyUpper:
        return track_name
    else:
        return None
