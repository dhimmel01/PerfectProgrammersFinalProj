# Import libraries for HTTP requests, data manipulation, and environment variables
import requests
import json
import os

# Import libraries for web scraping (if needed)
from bs4 import BeautifulSoup
import requests

# Import pandas for data manipulation
import pandas as pd

# Import SQLite for database interactions
import sqlite3

# Import libraries for visualization
import matplotlib.pyplot as plt



# Define a function to fetch data from an API
def fetch_data_from_api(url, params=None):
    """ Fetch data from an API and return the JSON response. """
    response = requests.get(url, params=params)
    return response.json()

# Define a function to connect to the SQLite database
def create_or_connect_database(db_file):
    """ Create a new SQLite database or connect to an existing one. """
    conn = sqlite3.connect(db_file)
    return conn

# Define a function to save data to the database
def save_data_to_database(conn, data, table_name):
    """ Save data to a specific table in the SQLite database. """
    pd.DataFrame(data).to_sql(table_name, conn, if_exists='append', index=False)

# Define a function to perform data visualization
def visualize_data(data, chart_type='bar'):
    """ Generate data visualization. """
    if chart_type == 'bar':
        data.plot(kind='bar')
        plt.show()
    elif chart_type == 'line':
        data.plot(kind='line')
        plt.show()
    # Add other chart types as necessary

def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    try:
        auth_response = requests.post(
            auth_url,
            auth=(client_id, client_secret),
            data={
                'grant_type': 'client_credentials'
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        auth_response.raise_for_status()  # Raises an exception for 4XX or 5XX errors
        auth_response_data = auth_response.json()
        return auth_response_data['access_token']
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_artist_data(artist_id, access_token):
    """Fetch data for a given artist using the Spotify Web API."""
    base_url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(base_url, headers=headers)
    return response.json()






# Beautiful Soup Billboard.com

def fetch_billboard_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    songs = soup.find_all('span', class_='chart-element__information__song')  # Modify as needed based on actual HTML structure
    artists = soup.find_all('span', class_='chart-element__information__artist')
    return [{'song': song.text, 'artist': artist.text} for song, artist in zip(songs, artists)]




if __name__ == '__main__':
    client_id = '67249b8fb9004c8fbe8f71b93b4b01fe'
    client_secret = '75f6662250a147298640a8d890957e3e'

    access_token = get_access_token(client_id, client_secret)
    if access_token:
        print("Access Token:", access_token)

        artist_id = '4Z8W4fKeB5YxbusRsdQVPb'  # Example: Spotify ID for the artist "Radiohead"
        artist_data = get_artist_data(artist_id, access_token)
        print("Artist Data:", artist_data)
    else:
        print("Failed to retrieve access token.")
