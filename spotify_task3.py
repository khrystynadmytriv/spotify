"""
This module creates a web
"""
import base64
from flask import Flask,render_template, request
import requests
from geopy.geocoders import Nominatim
import folium
import pycountry

CLIENT_ID = 'b2d4daf524d44f81a1d5902946f765ce'
CLIENT_SECRET = '2390f673b70f4e398cbb74b716c4208e'

def get_token():
    """
    returns a token
    """
    auth_code = f'{CLIENT_ID}:{CLIENT_SECRET}'
    coded_credentials = base64.b64encode(auth_code.encode()).decode()
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {'grant_type': 'client_credentials'}
    auth_headers = {'Authorization': f'Basic {coded_credentials}'}
    response = requests.post(auth_url, data = auth_data, headers=auth_headers,timeout=1)
    access_token = response.json()['access_token']
    return access_token

def artist(artist_name):
    """
    returns an artist id
    """
    base_url = 'https://api.spotify.com/v1'
    endpoint = '/search'
    search_url = f'{base_url}{endpoint}'
    request_params = {
        'query': artist_name,
        'type': 'artist'
    }
    request_headers = {'Authorization': f'Bearer {get_token()}'}
    response = requests.get(search_url, params=request_params, headers=request_headers,timeout=1)
    most_popular_artist = response.json().get('artists').get('items')[0]
    return most_popular_artist['id']

def track(artist_id):
    """
    returns track id
    """
    base_url = 'https://api.spotify.com/v1'
    endpoint = f'/artists/{artist_id}/top-tracks'
    search_url = f'{base_url}{endpoint}'
    request_params = {
        'query': artist_id,
        'market':'ES'
    }
    request_headers = {'Authorization': f'Bearer {get_token()}'}
    response = requests.get(search_url, params=request_params, headers=request_headers,timeout=1)
    most_popular_tracks = response.json().get('tracks')[0]
    return most_popular_tracks['id']

def markets(track_id):
    """
    returns avalible markets
    """
    base_url = 'https://api.spotify.com/v1'
    endpoint = f'/tracks/{track_id}'
    search_url = f'{base_url}{endpoint}'
    request_params = {
        'query': track_id,
    }
    request_headers = {'Authorization': f'Bearer {get_token()}'}
    response = requests.get(search_url, params=request_params, headers=request_headers,timeout=1)
    tracks = response.json()
    return tracks['available_markets']

def coor(available_markets):
    """
    returns the coordinates off avalible markets
    """
    coordinates = []
    geolocator = Nominatim(user_agent="locations")
    for i in available_markets:
        try:
            country = pycountry.countries.get(alpha_2=i)
            location = geolocator.geocode(country.name,timeout=10)
            coordinates.append([country.name,location.latitude,location.longitude])
        except AttributeError:
            continue
    return coordinates

def create_map(coordinates):
    """
    creates a map for the locations
    """
    map_songs = folium.Map()
    map_songs = folium.Map(tiles = 'Stamen Terrain')
    for i,j in enumerate(coordinates):
        map_songs.add_child(folium.Marker(location=coordinates[i][1:],
                                    popup=coordinates[i][0],
                                    icon=folium.Icon()))
    map_songs.save('templates/Map_Artist.html')
    return map_songs

app = Flask(__name__)
@app.route('/')

def index():
    """
    returns a html where you can put input
    """
    return render_template('index.html')

@app.route('/map', methods=("POST",'GET'))
def main():
    """
    main function that posts a map
    """
    if request.method == 'POST':
        artist_name = request.form.get('name')
        artist_id = artist(artist_name)
        track_id = track(artist_id)
        avalible_markets = markets(track_id)
        coordinates = coor(avalible_markets)
        song_map = create_map(coordinates)
        return render_template('map.html',map=song_map._repr_html_())

if __name__ == '__main__':
    app.run(debug=True)
