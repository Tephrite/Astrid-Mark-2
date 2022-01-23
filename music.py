import pandas as pd
from speech_recognition import Microphone, Recognizer, UnknownValueError
import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth


# Set variables from setup.txt
setup = pd.read_csv('Spotify/setup.txt', sep='=', index_col=0, squeeze=True, header=None)
client_id = setup['client_id']
client_secret = setup['client_secret']
device_name = setup['device_name']
redirect_uri = setup['redirect_uri']
scope = setup['scope']
username = setup['username']

# Connecting to the Spotify account
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    username=username)
spotify = sp.Spotify(auth_manager=auth_manager)

# Selecting device to play from
devices = spotify.devices()
deviceID = None
for d in devices['devices']:
    d['name'] = d['name'].replace('’', '\'')
    if d['name'] == device_name:
        deviceID = d['id']
        break
        
class InvalidSearchError(Exception):
    pass


def get_album_uri(spotify: sp, name: str) -> str:
    """
    :param spotify: Spotify object to make the search from
    :param name: album name
    :return: Spotify uri of the desired album
    """

    # Replace all spaces in name with '+'
    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='album')
    if not results['albums']['items']:
        raise InvalidSearchError(f'No album named "{original}"')
    album_uri = results['albums']['items'][0]['uri']
    return album_uri


def get_artist_uri(spotify: sp, name: str) -> str:
    """
    :param spotify: Spotify object to make the search from
    :param name: album name
    :return: Spotify uri of the desired artist
    """

    # Replace all spaces in name with '+'
    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='artist')
    if not results['artists']['items']:
        raise InvalidSearchError(f'No artist named "{original}"')
    artist_uri = results['artists']['items'][0]['uri']
    print(results['artists']['items'][0]['name'])
    return artist_uri


def get_track_uri(spotify: sp, name: str) -> str:
    """
    :param spotify: Spotify object to make the search from
    :param name: track name
    :return: Spotify uri of the desired track
    """

    # Replace all spaces in name with '+'
    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='track')
    if not results['tracks']['items']:
        raise InvalidSearchError(f'No track named "{original}"')
    track_uri = results['tracks']['items'][0]['uri']
    return track_uri


def play_album(spotify=None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, context_uri=uri)


def play_artist(spotify=None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, context_uri=uri)


def play_track(spotify=None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, uris=[uri])


def play_song(words):
    if len(words) <= 1:
        print('Could not understand. Try again')

    words.lower()
    
    if words.split()[0] == "play":
        name = words.split(" ", 1)[1]
        
    print(name)
    try:
        # if 'album' in words:
        #     uri = get_album_uri(spotify=spotify, name=name)
        #     play_album(spotify=spotify, device_id=deviceID, uri=uri)
        # elif 'artist' in words:
        #     uri = get_artist_uri(spotify=spotify, name=name)
        #     play_artist(spotify=spotify, device_id=deviceID, uri=uri)
        # elif 'play' in words:
        #     uri = get_track_uri(spotify=spotify, name=name)
        #     play_track(spotify=spotify, device_id=deviceID, uri=uri)
        # else:
        #     print('Specify either "album", "artist" or "play". Try Again')
        uri = get_track_uri(spotify=spotify, name=name)
        play_track(spotify=spotify, device_id=deviceID, uri=uri)
    except InvalidSearchError:
        print('InvalidSearchError. Try Again')
        
