import requests
import pandas as pd
import sqlite3

def create_or_connect_database(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_billboard_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS billboard_hot_100 (
            rank INTEGER,
            song TEXT,
            artist TEXT,
            last_week INTEGER,
            peak_position INTEGER,
            weeks_on_chart INTEGER,
            date TEXT
        );
    ''')
    conn.commit()

def fetch_billboard_data(date, start_rank):
    url = "https://billboard-api2.p.rapidapi.com/hot-100"
    headers = {
        "X-RapidAPI-Key": "4f2775e08emshb476776cc48055bp16752fjsn8b91ce849b8d",
        "X-RapidAPI-Host": "billboard-api2.p.rapidapi.com"
    }
    end_rank = start_rank + 24
    querystring = {"date": date, "range": f"{start_rank}-{end_rank}"}
    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()['content']
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def save_data_to_database(conn, data, date):
    cursor = conn.cursor()
    for rank, details in data.items():
        # Using the get method of dictionary to provide default values if keys are missing
        song = details.get('title', 'Unknown Title')
        artist = details.get('artist', 'Unknown Artist')
        last_week = details.get('last_week', None)  # None or appropriate default value
        peak_position = details.get('peak_position', None)
        weeks_on_chart = details.get('weeks_on_chart', None)

        cursor.execute('''
            INSERT INTO billboard_hot_100 (rank, song, artist, last_week, peak_position, weeks_on_chart, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (rank, song, artist, last_week, peak_position, weeks_on_chart, date))
    conn.commit()

def fetch_and_display_data(conn):
    cursor = conn.cursor()
    query = "SELECT * FROM billboard_hot_100"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)


import matplotlib.pyplot as plt


def create_or_connect_database(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def fetch_data_for_visualization(conn):
    """Fetch song and weeks on chart from the database for visualization, ensuring no None values."""
    cursor = conn.cursor()
    query = "SELECT song, weeks_on_chart FROM billboard_hot_100 WHERE weeks_on_chart IS NOT NULL ORDER BY weeks_on_chart DESC LIMIT 10"
    cursor.execute(query)
    data = cursor.fetchall()
    return data

def visualize_data(data):
    """Generate a bar chart from the fetched data, handling None values."""
    songs = [item[0] for item in data if item[1] is not None]  # Ensure no None values in weeks
    weeks = [item[1] for item in data if item[1] is not None]  # Ensure no None values in weeks

    if not weeks:  # Check if the list is empty after filtering
        print("No valid data to display.")
        return

    plt.figure(figsize=(10, 8))
    plt.barh(songs, weeks, color='skyblue')
    plt.xlabel('Weeks on Chart')
    plt.ylabel('Songs')
    plt.title('Top 10 Songs by Weeks on Billboard Hot 100')
    plt.gca().invert_yaxis()  # Reverse the order to have the longest on top
    plt.show()













def main():
    db_file = 'music_data.db'
    conn = create_or_connect_database(db_file)
    create_billboard_table(conn)
    
    date = "2019-05-11"  # You can adjust this or make it dynamic as needed
    start_rank = 1
    total_items_fetched = 0

    while total_items_fetched <= 100:
        data = fetch_billboard_data(date, start_rank)
        
        if data:
            save_data_to_database(conn, data, date)
            print(f"Data saved to database successfully for ranks {start_rank} to {start_rank + 24}.")
            total_items_fetched += len(data)
            start_rank += 25  # Increment to fetch the next batch
        else:
            print("No more data fetched or end of data.")
            break

    fetch_and_display_data(conn)  # Optionally display data
    conn.close()


    db_file = 'music_data.db'
    conn = create_or_connect_database(db_file)
    
    data = fetch_data_for_visualization(conn)
    if data:
        visualize_data(data)
    else:
        print("No data available for visualization.")

    conn.close()


if __name__ == '__main__':
    main()
