# import requests
# import pandas as pd
# import sqlite3

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

# def create_or_connect_database(db_file):
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
#         pd.DataFrame(artists_data).to_sql(table_name, conn, if_exists='replace', index=False)
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

# def view_database(db_file):
#     try:
#         conn = sqlite3.connect(db_file)
#         cursor = conn.cursor()

#         # Fetch all tables in the database
#         cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#         tables = cursor.fetchall()

#         # Display contents of each table
#         for table in tables:
#             table_name = table[0]
#             print(f"Contents of {table_name} table:")
#             cursor.execute(f"SELECT * FROM {table_name};")
#             rows = cursor.fetchall()
#             for row in rows:
#                 print(row)

#         conn.close()
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")

# def main():
#     client_id = '67249b8fb9004c8fbe8f71b93b4b01fe'
#     client_secret = '75f6662250a147298640a8d890957e3e'
#     db_file = 'spotify.db'
#     artist_ids = ['4Z8W4fKeB5YxbusRsdQVPb', '3TVXtAsR1Inumwj472S9r4', '0fA0VVWsXO9YnASrzqfmYu', '55Aa2cqylxrFIXC767Z865', 
#                    '66CXWjxzNUsdJxJ2JdwvnR', '06HL4z0CvFAxyc27GXpf02', '7dGJo4pcD2V6oG8kP0tJRR', '41X1TR6hrK8Q2ZCpp2EqCz',
#                    '4kYSro6naA4h99UJvo89HB', '181bsRPaVXVlUKXrxwZfHK', '5SXuuuRpukkTvsLuUknva1', '2YZyLoL8N0Wb9xBt1NhZWg',
#                    '77AiFEVeAVj2ORpC85QVJs', '0du5cEVh5yTK9QJze8zA0C', '7tYKF4w9nC0nq9CsPZTHyP', '246dkjvS1zLTtiykXe5h60',
#                    '5K4W6rqBFWDnAN6FQUkS6x', '1Xyo4u8uXC1ZmMpatF05PJ', '7c0XG5cIJTrrAgEC3ULPiq', '4LLpKhyESsyAXpc4laK94U',
#                    '1RyvyyTE3xzB2ZywiAwp0i', '5f7VJjfbwm532GiveGC0ZK', '6l3HvQ5sa6mXTsMTB19rO5', '4MCBfE4596Uoi2O4DtmEMz',
#                    '5cj0lLjcoR7YOSnhnX0Po5', '73sIBHcqh3Z3NyqHKZ7FOL', '0LcJLqbBmaGUft1e9Mm8HV', '1VPmR4DJC1PlOtd0IADAO0',
#                    '1ZwdS5xdxEREPySFridCfh', '7bXgB6jMjp9ATFy66eO08Z', '0YC192cP3KPCRWx8zr8MfZ', '4KWTAlx2RvbpseOGMEmROg',
#                    '2CvCyf1gEVhI0mX6aFXmVI', '44NX2ffIYHr6D4n7RaZF7A', '5f7VJjfbwm532GiveGC0ZK', '1sBkRIssrMs1AbVkOJbc7a',
#                    '3qiHUAX7zY4Qnjx8TNUzVx', '5me0Irg2ANcsgc93uaYrpb', '15UsOTVnJzReFVN1VCnxy4', '1mcTU81TzQhprhouKaTkpq',
#                    '2QsynagSdAqZj3U9HgDzjD', '6Ghvu1VvMGScGpOUJBAHNH', '0L8ExT028jH3ddEcZwqJJ5', '0vXtpskNA5slWYQBsjlaJU',
#                    '7wlFDEWiM5OoIAt8RSli8b', '7GlBOeep6PqTfFi59PTUUN', '6icQOAFXDZKsumw3YXyusw','23zg3TcAtWQy7J6upgbUnj', 
#                    '6qqNVTkY8uBg9cP3Jd7DAH', '3tlXnStJ1fFhdScmQeLpuG', '4oLeXFyACqeem2VImYeBFe', '1VPmR4DJC1PlOtd0IADAO0',
#                    '2HPaUgqeutzr3jx5a9WyDV', '6Xgp2XMz1fhVYe7i6yNAax', '5INjqkS1o8h1imAzPqGZBb', '3Nrfpe0tUJi4K4DXYWgMUX'
#                    '4dpARuHxo51G3z768sgnrY', '7n2wHs1TKAczGzO7Dd2rGr', '46SHBwWsqBkxI7EeeBEQG7', '1QAJqy2dA3ihHBFIHRphZj',
#                    '7wlFDEWiM5OoIAt8RSli8b', '0VRj0yCOv2FXJNP47XQnx5', '45TgXXqMDdF8BkjA83OM7z', '5he5w2lnU9x7JFhnwcekXX',
#                    '20JZFwl6HVl6yg8a4H3ZqK', '4tZwfgrHOc3mvqYlEYSvVi', '20qISvAhX20dpIbOOzGK3q', '2ye2Wgw4gimLv2eAKyk1NB',
#                    '5a2EaR3hamoenG9rDuVn8j', '1Mxqyy3pSjf8kZZL4QVxS0', '7FBcuc1gsnv6Y1nwFtNRCb',]

#     conn = create_or_connect_database(db_file)
#     access_token = get_access_token(client_id, client_secret)
#     if access_token:
#         print("Access Token retrieved successfully.")

#         # Fetch and save data for each artist ID
#         artist_data = get_artist_data(artist_ids, access_token)  # Get artist data
#         if artist_data:
#             save_data_to_database(conn, artist_data, 'artists')  # Save artist data
#             print("Data for artist IDs saved successfully.")

#             # Fetch data from the database
#             artists_data = fetch_data_from_database(conn)

#             # Display data
#             display_data(artists_data)

#         else:
#             print("No data found or failed to fetch data for artist IDs.")

#     else:
#         print("Failed to retrieve access token.")
#     conn.close()

# if __name__ == '__main__':
#     main()
#     view_database('spotify.db')


import requests
import pandas as pd
import sqlite3

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
    
    # Iterate through artist IDs in batches of 25
    for i in range(0, len(artist_ids), 25):
        batch_artist_ids = artist_ids[i:i+25]
        batch_data = []  # Store data for this batch
        
        # Fetch data for each artist ID in the batch
        for artist_id in batch_artist_ids:
            url = f'{base_url}{artist_id}'
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                artist = response.json()
                batch_data.append({
                    'id': artist['id'],
                    'name': artist['name'],
                    'followers': artist['followers']['total'],
                    'popularity': artist['popularity']
                })
            else:
                print(f"Failed to fetch data for artist ID: {artist_id}, Status Code: {response.status_code}")
        
        artist_data.extend(batch_data)  # Add batch data to main artist data
        
        # Check if we have already fetched 25 items
        if len(artist_data) >= 25:
            break
    
    return artist_data[:25]  # Return only the first 25 items


def save_data_to_database(conn, artists_data, table_name):
    try:
        # Insert 25 rows at a time
        for i in range(0, len(artists_data), 25):
            pd.DataFrame(artists_data[i:i+25]).to_sql(table_name, conn, if_exists='append', index=False)
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

def view_database(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Fetch all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Display contents of each table
        for table in tables:
            table_name = table[0]
            print(f"Contents of {table_name} table:")
            cursor.execute(f"SELECT * FROM {table_name};")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

def save_data_to_database(conn, artists_data, table_name):
    try:
        num_rows_before_insert = pd.read_sql_query(f"SELECT COUNT(*) FROM {table_name}", conn).iloc[0, 0]
        pd.DataFrame(artists_data).to_sql(table_name, conn, if_exists='append', index=False)
        num_rows_after_insert = pd.read_sql_query(f"SELECT COUNT(*) FROM {table_name}", conn).iloc[0, 0]
        num_rows_inserted = num_rows_after_insert - num_rows_before_insert
        print(f"{num_rows_inserted} rows inserted into {table_name} table.")
    except sqlite3.IntegrityError as e:
        print("Failed to insert data:", e)

def main():
    client_id = '67249b8fb9004c8fbe8f71b93b4b01fe'
    client_secret = '75f6662250a147298640a8d890957e3e'
    db_file = 'spotify.db'
    artist_ids = ['4Z8W4fKeB5YxbusRsdQVPb', '3TVXtAsR1Inumwj472S9r4', '0fA0VVWsXO9YnASrzqfmYu', '55Aa2cqylxrFIXC767Z865', 
                   '66CXWjxzNUsdJxJ2JdwvnR', '06HL4z0CvFAxyc27GXpf02', '7dGJo4pcD2V6oG8kP0tJRR', '41X1TR6hrK8Q2ZCpp2EqCz',
                   '4kYSro6naA4h99UJvo89HB', '181bsRPaVXVlUKXrxwZfHK', '5SXuuuRpukkTvsLuUknva1', '2YZyLoL8N0Wb9xBt1NhZWg',
                   '77AiFEVeAVj2ORpC85QVJs', '0du5cEVh5yTK9QJze8zA0C', '7tYKF4w9nC0nq9CsPZTHyP', '246dkjvS1zLTtiykXe5h60',
                   '5K4W6rqBFWDnAN6FQUkS6x', '1Xyo4u8uXC1ZmMpatF05PJ', '7c0XG5cIJTrrAgEC3ULPiq', '4LLpKhyESsyAXpc4laK94U',
                   '1RyvyyTE3xzB2ZywiAwp0i', '5f7VJjfbwm532GiveGC0ZK', '6l3HvQ5sa6mXTsMTB19rO5', '4MCBfE4596Uoi2O4DtmEMz',
                   '5cj0lLjcoR7YOSnhnX0Po5', '73sIBHcqh3Z3NyqHKZ7FOL', '0LcJLqbBmaGUft1e9Mm8HV', '1VPmR4DJC1PlOtd0IADAO0',
                   '1ZwdS5xdxEREPySFridCfh', '7bXgB6jMjp9ATFy66eO08Z', '0YC192cP3KPCRWx8zr8MfZ', '4KWTAlx2RvbpseOGMEmROg',
                   '2CvCyf1gEVhI0mX6aFXmVI', '44NX2ffIYHr6D4n7RaZF7A', '5f7VJjfbwm532GiveGC0ZK', '1sBkRIssrMs1AbVkOJbc7a',
                    '5me0Irg2ANcsgc93uaYrpb', '15UsOTVnJzReFVN1VCnxy4', '1mcTU81TzQhprhouKaTkpq', '4dpARuHxo51G3z768sgnrY', 
                    '7n2wHs1TKAczGzO7Dd2rGr', '46SHBwWsqBkxI7EeeBEQG7', '1QAJqy2dA3ihHBFIHRphZj',
                    '7wlFDEWiM5OoIAt8RSli8b', '0VRj0yCOv2FXJNP47XQnx5', '45TgXXqMDdF8BkjA83OM7z', '5he5w2lnU9x7JFhnwcekXX',
                   '20JZFwl6HVl6yg8a4H3ZqK', '4tZwfgrHOc3mvqYlEYSvVi', '20qISvAhX20dpIbOOzGK3q', '2ye2Wgw4gimLv2eAKyk1NB',
                   '5a2EaR3hamoenG9rDuVn8j', '1Mxqyy3pSjf8kZZL4QVxS0', '7FBcuc1gsnv6Y1nwFtNRCb'
                   '2QsynagSdAqZj3U9HgDzjD', '6Ghvu1VvMGScGpOUJBAHNH', '0L8ExT028jH3ddEcZwqJJ5', '0vXtpskNA5slWYQBsjlaJU',
                   '7wlFDEWiM5OoIAt8RSli8b', '7GlBOeep6PqTfFi59PTUUN', '6icQOAFXDZKsumw3YXyusw','23zg3TcAtWQy7J6upgbUnj', 
                   '6qqNVTkY8uBg9cP3Jd7DAH', '3tlXnStJ1fFhdScmQeLpuG', '4oLeXFyACqeem2VImYeBFe', '1VPmR4DJC1PlOtd0IADAO0',
                   '2HPaUgqeutzr3jx5a9WyDV', '6Xgp2XMz1fhVYe7i6yNAax', '5INjqkS1o8h1imAzPqGZBb', '3Nrfpe0tUJi4K4DXYWgMUX']

    conn = create_or_connect_database(db_file)
    access_token = get_access_token(client_id, client_secret)
    if access_token:
        print("Access Token retrieved successfully.")

        # Fetch and save data for each artist ID
        artist_data = get_artist_data(artist_ids, access_token)  # Get artist data
        if artist_data:
            save_data_to_database(conn, artist_data, 'artists')  # Save artist data
            print("Data for artist IDs saved successfully.")

            # Fetch data from the database
            artists_data = fetch_data_from_database(conn)

            # Display data
            display_data(artists_data)

        else:
            print("No data found or failed to fetch data for artist IDs.")

    else:
        print("Failed to retrieve access token.")
    conn.close()

if __name__ == '__main__':
    main()
    view_database('spotify.db')
