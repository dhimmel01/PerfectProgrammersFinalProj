import requests
import sqlite3
import os

def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    try:
        response = requests.post(
            auth_url,
            auth=(client_id, client_secret),
            data={'grant_type': 'client_credentials'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        response.raise_for_status()
        return response.json()['access_token']
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def create_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id TEXT PRIMARY KEY,  -- Change from INTEGER to TEXT
            name TEXT NOT NULL,
            followers INTEGER,
            popularity INTEGER
        );
    ''')

  
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY,
            artist_id TEXT,  -- Change from INTEGER to TEXT
            name TEXT NOT NULL,
            release_date TEXT,
            FOREIGN KEY (artist_id) REFERENCES artists(id)
        );
    ''')

    conn.commit()
    conn.close()

def get_artist_data(artist_ids, access_token):
    artist_data = []
    base_url = 'https://api.spotify.com/v1/artists/'
    headers = {'Authorization': f'Bearer {access_token}'}
    for artist_id in artist_ids:
        url = f'{base_url}{artist_id}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            artist = response.json()
            artist_data.append({
                'id': artist['id'],
                'name': artist['name'],
                'followers': artist['followers']['total'],
                'popularity': artist['popularity']
            })
        else:
            print(f"Failed to fetch data for artist ID: {artist_id}, Status Code: {response.status_code}")
    return artist_data

def get_artist_albums(artist_id, access_token):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/albums'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        albums_data = response.json().get('items', [])
        # Add artist ID to each album data
        for album in albums_data:
            album['artist_id'] = artist_id
        return albums_data
    else:
        print(f"Failed to fetch albums for artist ID: {artist_id}, Status Code: {response.status_code}")
        return []

def save_data_to_database(conn, artist_data, albums_data):
    try:
        cursor = conn.cursor()
        for artist in artist_data:
            cursor.execute('''
                INSERT OR IGNORE INTO artists (id, name, followers, popularity)
                VALUES (?, ?, ?, ?);
            ''', (artist['id'], artist['name'], artist['followers'], artist['popularity']))
        
        for album in albums_data:
            cursor.execute('''
                INSERT INTO albums (artist_id, name, release_date)
                VALUES (?, ?, ?);
            ''', (album['artist_id'], album['name'], album['release_date']))

        conn.commit()
        print("Data saved successfully.")
    except sqlite3.IntegrityError as e:
        print("Failed to insert data:", e)

def main():
    client_id = '67249b8fb9004c8fbe8f71b93b4b01fe'
    client_secret = '75f6662250a147298640a8d890957e3e'
    db_file = 'spotify.db'
    batch_size = 25
    
    create_database(db_file)  # Create the SQLite database with two tables

    conn = sqlite3.connect(db_file)
    access_token = get_access_token(client_id, client_secret)
    if access_token:
        print("Access Token retrieved successfully.")

        with open('artist_ids.txt', 'r') as f:
            artist_ids = [line.strip() for line in f if line.strip()]
            total_artists = len(artist_ids)

           
            index_file = 'last_index.txt'
            last_index = 0
            if os.path.exists(index_file):
                with open(index_file, 'r') as idx_f:
                    last_index = int(idx_f.read())

            
            start_index = last_index
            end_index = min(start_index + batch_size, total_artists)
            if start_index >= total_artists:
                print("All artists processed. Resetting...")
                with open(index_file, 'w') as idx_f:
                    idx_f.write('0')  
                conn.execute("DELETE FROM artists")  
                conn.execute("DELETE FROM albums")   
                conn.commit()
                return

           
            batch_artist_ids = artist_ids[start_index:end_index]
            for artist_id in batch_artist_ids:
                artist_data = get_artist_data([artist_id], access_token)
                albums_data = get_artist_albums(artist_id, access_token)
                if artist_data and albums_data:
                    save_data_to_database(conn, artist_data, albums_data)
                    print(f"Data for artist ID {artist_id} saved successfully.")

            
            with open(index_file, 'w') as idx_f:
                idx_f.write(str(end_index))

    else:
        print("Failed to retrieve access token.")
    conn.close()

if __name__ == '__main__':
    main()
