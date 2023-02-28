"""
This module return information about artist
"""
import base64
import requests


CLIENT_ID = 'b2d4daf524d44f81a1d5902946f765ce'
CLIENT_SECRET = '2390f673b70f4e398cbb41b716c4208e'

def get_token():
    """
    gets token
    """
    auth_code = f'{CLIENT_ID}:{CLIENT_SECRET}'
    coded_credentials = base64.b64encode(auth_code.encode()).decode()
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {'grant_type': 'client_credentials'}
    auth_headers = {'Authorization': f'Basic {coded_credentials}'}
    response = requests.post(auth_url, data = auth_data, headers=auth_headers,timeout=1)
    access_token = response.json()['access_token']
    return access_token

def artists():
    """
    return information about artist
    """
    artist_name = input()
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
    artist_id = most_popular_artist['id']
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    request_params = {
        'query': artist_id,
    }
    request_headers = {'Authorization': f'Bearer {get_token()}'}
    response = requests.get(url, params=request_params, headers=request_headers,timeout=1)
    artist = response.json()
    print(list(artist.keys()))
    key1 = input('chose your parameters:')
    if isinstance(artist[key1],dict):
        print(list(artist[key1].keys()))
        key2 = input('chose your parameters:')
        return artist[key1][key2]
    return artist[key1]

if __name__ == '__main__':
    print(artists())
