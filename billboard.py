import requests
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

def create_or_connect_database(db_file='spotify.db'):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank INTEGER,
            title TEXT,
            artist_id INTEGER,
            last_week INTEGER,
            peak_position INTEGER,
            weeks_on_chart INTEGER,
            UNIQUE(rank, title, artist_id)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS billboard_artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        );
    ''')
    conn.commit()
    return conn

def fetch_billboard_data(limit=25, offset=0):
    url = "https://billboard-api2.p.rapidapi.com/hot-100"
    headers = {
        "X-RapidAPI-Key": "4f2775e08emshb476776cc48055bp16752fjsn8b91ce849b8d",
        "X-RapidAPI-Host": "billboard-api2.p.rapidapi.com"
    }
    query = {"date": "2019-05-11", "range": f"{offset+1}-{offset+limit}"}
    response = requests.get(url, headers=headers, params=query)
    data = []
    if response.status_code == 200:
        content = response.json().get('content', {})
        for key, item in content.items():
            try:
                rank = int(item.get('rank', 0))
                title = item.get('title', "")
                artist = item.get('artist', "")
                last_week = int(item.get('last week', '0').replace('-', '0'))
                peak_position = int(item.get('peak position', '0').replace('-', '0'))
                weeks_on_chart = int(item.get('weeks on chart', '0').replace('-', '0'))
                data.append((rank, title, artist, last_week, peak_position, weeks_on_chart))
            except ValueError:
                continue
    else:
        print(f"Failed to fetch data, Status Code: {response.status_code}")
    return data

def save_data_to_database(conn, data):
    cursor = conn.cursor()
    for record in data:
        cursor.execute('''
            INSERT OR IGNORE INTO billboard_artists (name) VALUES (?)
        ''', (record[2],))
        cursor.execute('''
            SELECT id FROM billboard_artists WHERE name = ?
        ''', (record[2],))
        artist_id = cursor.fetchone()[0]
        cursor.execute('''
            INSERT OR IGNORE INTO songs (rank, title, artist_id, last_week, peak_position, weeks_on_chart)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (record[0], record[1], artist_id, record[3], record[4], record[5]))
    conn.commit()

def query_data_and_write_to_file():
    conn = sqlite3.connect('spotify.db')# Connect to the Billboard database
    cursor = conn.cursor()
    query = """
    SELECT a.name, COUNT(*) as song_count
    FROM songs s
    JOIN billboard_artists a ON s.artist_id = a.id
    GROUP BY a.name
    ORDER BY song_count DESC
    """
    results = cursor.execute(query).fetchall()
    with open('artist_song_counts.txt', 'w') as file:
        for result in results:
            file.write(f"Artist: {result[0]}, Songs on Chart: {result[1]}\n")
    conn.close()


def visualize_data(db_file='spotify.db'):
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query("SELECT peak_position, weeks_on_chart, title FROM songs", conn)
    conn.close()

    top_20 = df.nlargest(20, 'weeks_on_chart').sort_values('weeks_on_chart', ascending=True)

    plt.figure(figsize=(12, 8))
    plt.scatter(top_20['weeks_on_chart'], top_20['peak_position'], alpha=0.5, color='orange')  # Changed color to orange
    plt.xlabel('Weeks on Chart')
    plt.ylabel('Chart Ranking')
    plt.title('Top 20 Songs by Longevity and Chart Success (May 2019)')
    plt.gca().invert_yaxis()
    plt.show()

    # Second Visualization: Horizontal Bar Chart of the Top 20
    plt.figure(figsize=(12, 8))
    plt.barh(top_20['title'], top_20['weeks_on_chart'], color='green')  # Changed color to green
    plt.xlabel('Weeks on Chart')
    plt.ylabel('Songs')
    plt.title('Top 20 Songs by Weeks on Chart (May 2019)')
    plt.tight_layout()
    plt.show()



def reset_state():
    if os.path.exists('state.json'):
        os.remove('state.json')
    if os.path.exists('spotify.db'):
        os.remove('spotify.db')
    print("Reset complete. Ready to start fetching data from scratch.")

def load_state():
    try:
        with open('state.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'total_records': 0, 'offset': 0}

def save_state(state):
    with open('state.json', 'w') as f:
        json.dump(state, f)

def main():
    conn = create_or_connect_database()
    state = load_state()
    if state['total_records'] >= 100:
        print("Resetting after 100 records.")
        reset_state()
        conn = create_or_connect_database()
        state = {'total_records': 0, 'offset': 0}

    data = fetch_billboard_data(limit=25, offset=state['offset'])
    if data:
        save_data_to_database(conn, data)
        state['total_records'] += len(data)
        state['offset'] += 25
        save_state(state)
        print(f"Fetched {len(data)} records, total fetched: {state['total_records']}.")
        visualize_data()
        query_data_and_write_to_file()
    else:
        print("No data fetched in this run.")

    conn.close()

if __name__ == "__main__":
    main()
