
# import requests
# import pandas as pd
# import sqlite3
# import os

# def get_access_token(client_id, client_secret):
#     auth_url = 'https://accounts.spotify.com/api/token'
#     try:
#         response = requests.post(
#             auth_url,
#             auth=(client_id, client_secret),
#             data={'grant_type': 'client_credentials'},
#             headers={'Content-Type': 'application/x-www-form-urlencoded'}
#         )
#         response.raise_for_status()
#         return response.json()['access_token']
#     except requests.RequestException as e:
#         print(f"An error occurred: {e}")
#         return None

# def create_or_reset_database(db_file):
#     if os.path.exists(db_file):
#         os.remove(db_file)
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS artists (
#             id TEXT PRIMARY KEY,
#             name TEXT NOT NULL,
#             followers INTEGER,
#             popularity INTEGER
#         );
#     ''')
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS tracks (
#             id TEXT PRIMARY KEY,
#             artist_id TEXT NOT NULL,
#             name TEXT,
#             popularity INTEGER,
#             duration_ms INTEGER,
#             explicit BOOLEAN,
#             preview_url TEXT,
#             FOREIGN KEY (artist_id) REFERENCES artists(id)
#         );
#     ''')
#     conn.commit()
#     return conn

# def get_artist_data(artist_ids, access_token):
#     artist_data = []
#     base_url = 'https://api.spotify.com/v1/artists/'
#     headers = {'Authorization': f'Bearer {access_token}'}
#     for artist_id in artist_ids:
#         url = f'{base_url}{artist_id}'
#         response = requests.get(url, headers=headers)
#         if response.status_code == 200:
#             artist = response.json()
#             artist_data.append({
#                 'id': artist['id'],
#                 'name': artist['name'],
#                 'followers': artist['followers']['total'],
#                 'popularity': artist['popularity']
#             })
#         else:
#             print(f"Failed to fetch data for artist ID: {artist_id}, Status Code: {response.status_code}")
#     return artist_data

# def save_data_to_database(conn, artists_data, table_name):
#     try:
#         pd.DataFrame(artists_data).to_sql(table_name, conn, if_exists='append', index=False)
#     except sqlite3.IntegrityError as e:
#         print("Failed to insert data:", e)

# def fetch_data_from_database(conn):
#     data = pd.read_sql_query("SELECT * FROM artists", conn)
#     return data

# def display_data(artists_data):
#     print("ID\t\tName\t\t\tFollowers\tPopularity")
#     print("-" * 80)
#     for index, artist_row in artists_data.iterrows():
#         print(f"{artist_row['id']}\t{artist_row['name']:<20}\t{artist_row['followers']:<10}\t{artist_row['popularity']}")

# def main():
#     client_id = '67249b8fb9004c8fbe8f71b93b4b01fe'
#     client_secret = '75f6662250a147298640a8d890957e3e'
#     db_file = 'spotify.db'
#     batch_size = 25
    
#     conn = create_or_reset_database(db_file)
#     access_token = get_access_token(client_id, client_secret)
#     if access_token:
#         print("Access Token retrieved successfully.")

#         with open('artist_ids.txt', 'r') as f:
#             artist_ids = [line.strip() for line in f if line.strip()]
#             total_artists = len(artist_ids)

#             # Check if index file exists
#             index_file = 'last_index.txt'
#             last_index = 0
#             if os.path.exists(index_file):
#                 with open(index_file, 'r') as idx_f:
#                     last_index = int(idx_f.read())

#             # Calculate next batch start and end index
#             start_index = last_index
#             end_index = min(start_index + batch_size, total_artists)
#             if start_index >= total_artists:
#                 print("All artists processed. Resetting database and starting again.")
#                 conn.close()
#                 conn = create_or_reset_database(db_file)
#                 start_index = 0
#                 end_index = min(batch_size, total_artists)

#             # Fetch and save data for each batch of artist IDs
#             batch_artist_ids = artist_ids[start_index:end_index]
#             artist_data = get_artist_data(batch_artist_ids, access_token)
#             if artist_data:
#                 save_data_to_database(conn, artist_data, 'artists')
#                 print(f"Data for artist IDs {start_index+1} to {end_index} saved successfully.")

#                 # Update last index file
#                 with open(index_file, 'w') as idx_f:
#                     idx_f.write(str(end_index))
#             else:
#                 print(f"No data found or failed to fetch data for artist IDs {start_index+1} to {end_index}.")

#         # Fetch all data from the database
#         artists_data = fetch_data_from_database(conn)

#         # Display all data
#         display_data(artists_data)

#     else:
#         print("Failed to retrieve access token.")
#     conn.close()

# if __name__ == '__main__':
#     main()





import requests
import pandas as pd
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

def create_or_connect_database(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            followers INTEGER,
            popularity INTEGER
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            id TEXT PRIMARY KEY,
            artist_id TEXT NOT NULL,
            name TEXT,
            popularity INTEGER,
            duration_ms INTEGER,
            explicit BOOLEAN,
            preview_url TEXT,
            FOREIGN KEY (artist_id) REFERENCES artists(id)
        );
    ''')
    conn.commit()
    return conn

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

def save_data_to_database(conn, artists_data, table_name):
    try:
        pd.DataFrame(artists_data).to_sql(table_name, conn, if_exists='append', index=False)
    except sqlite3.IntegrityError as e:
        print("Failed to insert data:", e)

def fetch_data_from_database(conn):
    data = pd.read_sql_query("SELECT * FROM artists", conn)
    return data

def display_data(artists_data):
    print("ID\t\tName\t\t\tFollowers\tPopularity")
    print("-" * 80)
    for index, artist_row in artists_data.iterrows():
        print(f"{artist_row['id']}\t{artist_row['name']:<20}\t{artist_row['followers']:<10}\t{artist_row['popularity']}")

def main():
    client_id = '67249b8fb9004c8fbe8f71b93b4b01fe'
    client_secret = '75f6662250a147298640a8d890957e3e'
    db_file = 'spotify.db'
    batch_size = 25
    
    conn = create_or_connect_database(db_file)
    access_token = get_access_token(client_id, client_secret)
    if access_token:
        print("Access Token retrieved successfully.")

        with open('artist_ids.txt', 'r') as f:
            artist_ids = [line.strip() for line in f if line.strip()]
            total_artists = len(artist_ids)

            # Check if index file exists
            index_file = 'last_index.txt'
            last_index = 0
            if os.path.exists(index_file):
                with open(index_file, 'r') as idx_f:
                    last_index = int(idx_f.read())

            # Calculate next batch start and end index
            start_index = last_index
            end_index = min(start_index + batch_size, total_artists)
            if start_index >= total_artists:
                print("All artists processed. Resetting...")
                with open(index_file, 'w') as idx_f:
                    idx_f.write('0')  # Reset index to 0
                conn.execute("DELETE FROM artists")  # Clear artists table
                conn.commit()
                return

            # Fetch and save data for each batch of artist IDs
            batch_artist_ids = artist_ids[start_index:end_index]
            artist_data = get_artist_data(batch_artist_ids, access_token)
            if artist_data:
                save_data_to_database(conn, artist_data, 'artists')
                print(f"Data for artist IDs {start_index+1} to {end_index} saved successfully.")

                # Update last index file
                with open(index_file, 'w') as idx_f:
                    idx_f.write(str(end_index))
            else:
                print(f"No data found or failed to fetch data for artist IDs {start_index+1} to {end_index}.")

        # Fetch all data from the database
        artists_data = fetch_data_from_database(conn)

        # Display all data
        display_data(artists_data)

    else:
        print("Failed to retrieve access token.")
    conn.close()

if __name__ == '__main__':
    main()
